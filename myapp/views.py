from django.shortcuts import render,resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


# 記事一覧を表示
class Index(TemplateView):
  template_name = 'myapp/index.html'

  def get_context_data(self, *args, **kwargs):
    # contextとして取得（テンプレ）
    context = super().get_context_data(**kwargs)

    # Postの内容を取得　Post.objects.all()で全て取得
    post_list = Post.objects.all().order_by('-created_at')

    # viewへcontextを渡す
    context = {
      'post_list' : post_list,
    }
    return context

# 記事作成
class PostCreate(LoginRequiredMixin,CreateView):
  model = Post
  form_class = PostForm
  # Postが成功した場合、indexへ遷移する
  success_url = reverse_lazy('myapp:index')

  def form_valid(self, form):
    # author_id に pkを格納
    form.instance.author_id = self.request.user.id
    return super(PostCreate, self).form_valid(form)  # PostCreateを更新

  def get_success_url(self):
    messages.info(self.request, '投稿しました。')
    return resolve_url('myapp:index')

class PostDetail(DetailView):
  model = Post

class PostUpdate(LoginRequiredMixin,UpdateView):
  model = Post
  form_class = PostForm
  def get_success_url(self):
    messages.info(self.request, '更新しました')
    return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])

class PostDelete(LoginRequiredMixin,DeleteView):
  model = Post
  def get_success_url(self):
    messages.info(self.request, '投稿を削除しました。')
    return resolve_url('myapp:index')

class PostList(ListView):
  model = Post
  # 投稿日時で並び変えて取得
  def get_queryset(self):
    return Post.objects.all().order_by('-created_at')

class Login(LoginView):
  form_class = LoginForm
  template_name = 'myapp/login.html'

class Logout(LogoutView):
  template_name = 'myapp/logout.html'

class SignUp(CreateView):
  form_class = SignUpForm
  template_name = 'myapp/signup.html'
  success_url = reverse_lazy('myapp:index')

  # フォームの内容が有効だった場合の処理
  def form_valid(self, form):

    # フォームの内容をuser変数に格納
    user = form.save()
    # userを引数として、ログイン処理を実行
    login(self.request, user)
    self.object = user

    messages.info(self.request, 'ユーザー登録が完了しました。')
    return HttpResponseRedirect(self.get_success_url())
