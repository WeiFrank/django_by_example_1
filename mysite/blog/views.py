from django.shortcuts import render,get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from blog.models import Post,Comment
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm
from haystack.query import SearchQuerySet
# Create your views here.
#def post_list(request):
#	posts = Post.published.all()
#	print(posts)
#	return render(request,'post/list.html',{'posts':posts})

#def post_detail(request, year, month, day, post):
#	p=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
#	print(p)
#	return render(request,
#			'post/detail.html',
#			{'post': p})
def post_detail(request,year,post):
	post=get_object_or_404(Post,publish__year=year,slug=post)
	comments = post.comments.filter(active=True)
	new_comment=''
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to the database
			new_comment.save()
	else:
		comment_form = CommentForm()
	# List of similar posts
	#>>>post.tags.values_list('id',flat=True) will return the id number of the post's tag
	#>>>[2, 3] #tag's id
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	#exclude post's self tag id 
	#similar_posts = Post.published.filter(tags__in=lid).exclude(id=post.id)
	# output :[<Post: test>]
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
	return render(request,'post/detail.html',{'post': post,'comments': comments,'comment_form': comment_form,\
			'new_comment':new_comment,'similar_posts':similar_posts})
	#print(p)
	#return render(request,'post/detail.html',{'post': p})
def post_list(request,tag_slug=	None):
	object_list=Post.published.all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list,2)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
		print(posts)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request,'post/list.html',{'posts':posts,'page':page,'tag':tag})
class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'post/list.html'
def post_share(request,post_id):
	post = get_object_or_404(Post,id=post_id,status='published')
	sent = False
	re = None
	if request.method == 'POST':
		#Form fields passed validation
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			request.session['name'] = cd['name']
			request.session['email'] = cd['email']
			request.session['to'] = cd['to']
			#print(session.get['to'])
			post_url =request.build_absolute_uri(post.get_absolute_url())
			print(post_url)
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
			message = 'Read"{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
			re = cd['to']
			print(re)
			send_mail(subject, message, 'zhuwei2013131018@sina.com',[cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	#return render(request, 'post/share.html', {'post': post,'form':form,'sent':sent,'cd':re})
	return render(request, 'post/share.html', {'post': post,'form':form,'sent':sent})
def post_search(request):
	form = SearchForm()
	print(form)
	cd = None
	results = ''
	total_results= ''
	exist =''
	if 'query' in request.GET:
		exist = True
		form = SearchForm(request.GET)
		if form.is_valid():
			cd = form.cleaned_data
			results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
		# count total results
			total_results = results.count()
			#print(total_results)
	return render(request,'post/search.html',{'form': form,
			'cd': cd,'results': results,'total_results': total_results,'exist':exist})
