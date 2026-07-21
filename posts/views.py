from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import PostForm, CommentForm


@login_required
def feed(request):
    # Get posts from users the current user follows + own posts
    following_profiles = request.user.profile.following.all()
    following_users = User.objects.filter(
        profile__in=following_profiles
    )

    posts = Post.objects.filter(
        user__in=list(following_users) + [request.user]
    ).select_related('user', 'user__profile').prefetch_related(
        'likes', 'comments'
    ).order_by('-created_at')

    # If no posts in feed, show all posts
    if not posts.exists():
        posts = Post.objects.all().select_related(
            'user', 'user__profile'
        ).prefetch_related('likes', 'comments').order_by('-created_at')

    post_form = PostForm()
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
    }
    return render(request, 'posts/feed.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('posts:feed')
        else:
            messages.error(request, 'Please add text or an image.')
    return redirect('posts:feed')


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related(
        'user', 'user__profile'
    )
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('posts:post_detail', post_id=post.id)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    # Return JSON for AJAX or redirect for normal request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'count': post.get_likes_count()
        })

    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {
        'form': form,
        'post': post
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('posts:feed')


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    post_id = comment.post.id
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('posts:post_detail', post_id=post_id)