from django.contrib.sitemaps import Sitemap
from .models import Post
class PostSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.9
	protocol='https'
	#limit = 2
	def items(self):
		return Post.published.all()
	def lastmod(self, obj):
		return obj.publish
#	def location(self,obj):
#		return '/192.168.19.155:9000/ %s' % + obj.get_absolute_url()
	def priority(self,obj):
		return '0.5'
