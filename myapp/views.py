from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm


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
