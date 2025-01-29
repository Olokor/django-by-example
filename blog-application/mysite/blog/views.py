from django.http import Http404
from django.shortcuts import render, get_list_or_404
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.publised.all()
    return render(
        request, "blog/post/list.html", {"posts":posts}
    )

def post_detail(request, id):
    # try:
    #     post = Post.publised.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post Found")

    post = get_list_or_404(Post, id=id, status=Post.Status.Published)
    return render(request, 'blog/post/detail.html', {"post":post})
