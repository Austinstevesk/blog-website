from django.shortcuts import render, get_object_or_404
'''Returns object or 404 error
if the object does not exist'''
from django.http import HttpResponse
#Mixins works as login required but with class based views
#Our PostCreateView is class based so we have to use it
#Note the prular while importing but singular while using it 
#UserPassesTestMixin ensures that only the author of a post can update it
#It needs a function created which runs to test if the user is the author
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
	)
from .models import Post
from django.contrib.auth.models import User


# Create your views here.



'''def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blogapp/home.html', context)'''

#works as the new homepage 
class PostListView(ListView):
	model = Post
	template_name = 'blogapp/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts' #Getting the data in the home view from the db
	ordering = ['-date_posted'] #order posts from newest to oldest

	paginate_by = 5 #The number of posts we have per page

class UserPostListView(ListView):
	model = Post
	template_name = 'blogapp/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts' #Getting the data in the home view from the db
	ordering = ['-date_posted'] #order posts from newest to oldest

	paginate_by = 5 #The number of posts we have per page

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

#Details for the post
class PostDetailView(DetailView):
	model = Post

#Creating a post
#Mixins should be at the left
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	def form_valid(self, form):
		"""setting the author of a post to the current logged in author before
		submitting the form so as the post can have an author before being created"""
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	def form_valid(self, form):
	   form.instance.author = self.request.user
	   return super().form_valid(form)

	#test function for UserPassesTestMixin
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

#Deleting posts
#You need a success url to be redirected to
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post

	success_url ='/'#Redirected to home after deleting the post
	#test function for UserPassesTestMixin
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def about(request):
	return render(request, 'blogapp/about.html', {'title': 'About Austin'})

def contact(request):
	return render(request, 'blogapp/contact.html')