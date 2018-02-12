from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post
from blog.forms import PostForm
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

