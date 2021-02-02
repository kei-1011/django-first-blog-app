from django.shortcuts import render,resolve_url
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView


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
class PostCreate(CreateView):
  model = Post
  form_class = PostForm
  # Postが成功した場合、indexへ遷移する
  success_url = reverse_lazy('myapp:index')

class PostDetail(DetailView):
  model = Post

class PostUpdate(UpdateView):
  model = Post
  form_class = PostForm
  def get_success_url(self):
    messages.info(self.request, '更新しました')
    return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])

class PostDelete(DeleteView):
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
