from django import forms
from .models import Post


class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'content')

# 　class呼び出し時に実行
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # 各フィールドにクラスを付与
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'
