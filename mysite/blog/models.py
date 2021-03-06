from django.db import models
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status='published')
class  Post(models.Model):
	#The  tags manager will allow you to add, retrieve, and remove tags from Post objects.
	tags = TaggableManager()
	objects = models.Manager() # The default manager.#Post.objects.all()...and so on.
	published = PublishedManager() # Our custom manager.use:Post.published.[all(),filter()] and so on.
	STATUS_CHOICES = (
			('draft','Draft'),
			('published','Published'),
			)
	title = models.CharField(max_length=10)
	slug = models.SlugField(max_length=250,unique_for_date='publish')
	author = models.ForeignKey(User,related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
	class Meta:
		ordering = ('-publish',)
	def __str__(self):
		return self.title
	#def get_absolute_url(self):
	#	return reverse('blog:post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[self.publish.year,self.slug])
class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	class Meta:
		ordering = ('created',)
	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)

