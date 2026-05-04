from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Comment
from .forms import CommentForm

# Create your views here.
def post_list(request): # "all functions in views take a request"
    # return requested html page and data
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts' : posts})

#create a post detail function to search by id and grab ONE item or return a 404
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm

    return render(request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts' : posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect('post_list')

def logout_view(request):
    logout(request)
    return redirect('post_list')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm

    return render(request, 'blog/add_comment_to_post.html', {'form' : form})