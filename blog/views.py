from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def is_authorized(func):
    def auth_dec(*args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        if args[0].user == post.author:
            ret_val = func(*args, **kwargs)
            return ret_val
        else:
            return HttpResponseForbidden()
    return auth_dec

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect('post_detail', pk=post.pk)

# Create your views here.
@login_required
def post_list(request):
    posts = Post.objects.all()
    #form = PostForm(request.POST)
    if posts:
        return render(request, 'blog/post_list.html', {'posts':posts})
    else:
        return redirect('post_new')

def post_detail(request, pk):
    edit = False
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        edit = True
    return render(request, 'blog/post_detail.html', {'post': post, "edit": edit})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
@is_authorized
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def list_category(request, type):
    result_dict = {}
    if type == "0":
        posts = Post.objects.all()
        for i in range(1,5):
                result_dict["{}".format(i)] = len(posts.filter(category=i))
    
    return render(request, 'blog/categories.html', {"result_dict":result_dict, "posts":posts})

def mypost(request):
    # posts = get_list_or_404(Post, author=request.user)
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/post_list.html', {"posts": posts})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
