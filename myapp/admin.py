from django.contrib import admin

# 同階層のmodelからPostをインポート
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'created_at')
  list_display_links = ('title',)
  ordering = ('-created_at',)
