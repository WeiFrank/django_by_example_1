from django.contrib import admin
from blog.models import Post
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'publish','status')
	list_filter = ('status', 'created', 'publish', 'author')
	search_fields = ('title', 'body')
	ordering = ['status', 'publish']
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
from .models import Post, Comment
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post,PostAdmin)
