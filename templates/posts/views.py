from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def feed(request, post_id=None):
    return render(request, 'posts/feed.html')