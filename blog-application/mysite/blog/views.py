from tkinter.font import names

from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.template.context_processors import request

from .form import EmailPostForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

# Create your views here.

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{form_data['name']} ({form_data['email']}) recommends you read {post.title}"
            )

            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{form_data['name']}'s comment: {form_data['comment']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # Use a valid email
                recipient_list=[form_data["recipient"]],
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
class PostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = "blog/post/list.html"
    context_object_name = "posts"
def post_list(request):
    all_posts = Post.published.all()
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request, "blog/post/list.html", {"posts":posts}
    )

def post_detail(request, year, month, day, post ):
    # try:
    #     post = Post.publised.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post Found")

    post = get_object_or_404(Post,  status=Post.Status.PUBLISHED,
                           slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {"post":post})
