from django.shortcuts import render,resolve_url, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post, Like, Category
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

class OnlyMyPostMixin(UserPassesTestMixin):
  raise_exception = True
  def test_func(self):
    # 記事オブジェクトをpostに格納
    post = Post.objects.get(id=self.kwargs['pk'])
    # 記事のauthorがログインしているユーザーかどうかを判断
    return post.author == self.request.user


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
  # DetailViewから渡されたデータはobjectという名称になる

  def get_context_data(self, **kwargs):
    # 表示している記事の詳細データを取得
    detail_data = Post.objects.get(id=self.kwargs['pk'])

    # 同じカテゴリーに属する記事を取得 [:5]で先頭から５件
    category_posts = Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5]
    params = {
      'object': detail_data,
      'category_posts':category_posts,
    }
    return params

class PostUpdate(OnlyMyPostMixin,UpdateView):
  model = Post
  form_class = PostForm
  def get_success_url(self):
    messages.info(self.request, '更新しました')
    return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])

class PostDelete(OnlyMyPostMixin,DeleteView):
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

# ログイン状態でないと動作しない
# defの場合は　login_required を使う
@login_required
def Like_add(request, post_id):
  post = Post.objects.get(id=post_id)
  #　ログイン中のユーザーで、現在開いている投稿にLikeされているかを確認する
  is_like = Like.objects.filter(user = request.user).filter(post = post_id).count()
  if is_like > 0:
    messages.info(request, 'すでにお気に入りに追加済みです。')
    return redirect('myapp:post_detail', post.id)

  like = Like()
  like.user = request.user
  like.post = post
  like.save()

  messages.success(request, 'お気に入りに追加しました。')
  return redirect('myapp:post_detail', post.id)


class CategoryList(ListView):
  model = Category


class CategoryDetail(DetailView):
  model = Category
  slug_field = 'name_en'
  slug_url_kwarg = 'name_en'

  def get_context_data(self, *args, **kwargs):
    # contextとして取得（テンプレ）
    context = super().get_context_data(**kwargs)

    # Postの内容を取得　Post.objects.all()で全て取得
    detail_data = Category.objects.get(name_en=self.kwargs['name_en'])
    category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')

    params = {
      'object': detail_data,
      'category_posts':category_posts,
    }
    return params
