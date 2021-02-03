from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
  name = models.CharField("カテゴリ名", max_length=50)
  name_en = models.CharField("カテゴリ名英語", max_length=10)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
  # Postを参照するとき、タイトルを指定して参照できる
    return self.name

# Post
class Post(models.Model):
  # user ForeignKey→外部キー
  author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)

  # タイトルを指定、最大文字数を５０文字
  title = models.CharField('タイトル', max_length=50)

  # コンテンツ
  content = models.TextField('内容', max_length=1000)

  # カテゴリ
  category = models.ForeignKey('Category', on_delete=models.PROTECT)

  # 画像
  thumbnail = models.ImageField(upload_to='images/',blank=True)

  # 現在の日時を保存
  created_at = models.DateTimeField(auto_now_add=True)

  # 更新された時に今の時刻を追加
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
  # Postを参照するとき、タイトルを指定して参照できる
    return self.title

class Like(models.Model):
  post = models.ForeignKey(Post, verbose_name="投稿", on_delete=models.PROTECT)
  user = models.ForeignKey(User, verbose_name="Likeしたユーザー", on_delete=models.PROTECT)
