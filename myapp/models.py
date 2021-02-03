from django.db import models
from django.contrib.auth.models import User
# Post
class Post(models.Model):
  # user ForeignKey→外部キー
  author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)

  # タイトルを指定、最大文字数を５０文字
  title = models.CharField('タイトル', max_length=50)

  # コンテンツ
  content = models.TextField('内容', max_length=1000)

  # 現在の日時を保存
  created_at = models.DateTimeField(auto_now_add=True)

  # 更新された時に今の時刻を追加
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
  # Postを参照するとき、タイトルを指定して参照できる
    return self.title
