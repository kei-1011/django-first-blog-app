from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Post

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
