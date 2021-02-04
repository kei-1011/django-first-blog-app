from django.contrib import admin
from django.contrib.sites.models import Site
from .models import SiteConfig

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
  list_display = ('id', 'meta_title', 'meta_description',)
  list_display_links = ('meta_title',)
