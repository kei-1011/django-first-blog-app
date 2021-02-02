from django.shortcuts import render,resolve_url
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib import messages

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
