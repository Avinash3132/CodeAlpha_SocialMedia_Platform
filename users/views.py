from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def register_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            tokens = get_tokens_for_user(user)
            messages.success(
                request,
                f'Welcome to ConnectHub, {user.first_name}! 🎉'
            )
            response = redirect('posts:feed')
            response.set_cookie(
                'access_token', tokens['access'],
                httponly=True, samesite='Lax'
            )
            response.set_cookie(
                'refresh_token', tokens['refresh'],
                httponly=True, samesite='Lax'
            )
            return response
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                tokens = get_tokens_for_user(user)
                messages.success(
                    request,
                    f'Welcome back, {user.first_name or user.username}! 👋'
                )
                next_url = request.GET.get('next', 'posts:feed')
                response = redirect(next_url)
                response.set_cookie(
                    'access_token', tokens['access'],
                    httponly=True, samesite='Lax'
                )
                response.set_cookie(
                    'refresh_token', tokens['refresh'],
                    httponly=True, samesite='Lax'
                )
                return response
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm(request)

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    response = redirect('users:login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    messages.success(request, 'Logged out successfully.')
    return response


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)

    try:
        posts = profile_user.posts.all().select_related(
            'user', 'user__profile'
        ).prefetch_related('likes', 'comments').order_by('-created_at')
    except AttributeError:
        posts = []

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = request.user.profile.is_following(profile)

    # Get followers and following lists
    followers = profile.followers.all().select_related('user')
    following = profile.following.all().select_related('user')

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'is_own_profile': request.user == profile_user,
        'followers': followers,
        'following': following,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES,
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile', username=request.user.username)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = get_object_or_404(Profile, user=target_user)
    my_profile = request.user.profile

    if request.user == target_user:
        messages.warning(request, "You can't follow yourself!")
        return redirect('users:profile', username=username)

    if my_profile.is_following(target_profile):
        my_profile.following.remove(target_profile)
        following = False
        messages.success(
            request,
            f'Unfollowed @{target_user.username}'
        )
    else:
        my_profile.following.add(target_profile)
        following = True
        messages.success(
            request,
            f'You are now following @{target_user.username}! 🎉'
        )

    # Return JSON for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'following': following,
            'followers_count': target_profile.get_followers_count()
        })

    return redirect('users:profile', username=username)


@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(
            id=request.user.id
        ).select_related('profile')[:20]

        # Annotate with following status
        my_profile = request.user.profile
        for u in users:
            u.is_followed = my_profile.is_following(u.profile)

    return render(request, 'users/search.html', {
        'query': query,
        'users': users,
    })


@login_required
def suggested_users(request):
    """Users not yet followed."""
    my_following = request.user.profile.following.all()
    suggestions = Profile.objects.exclude(
        id__in=my_following
    ).exclude(
        user=request.user
    ).select_related('user').order_by('?')[:6]

    return render(request, 'users/suggested.html', {
        'suggestions': suggestions
    })


@login_required
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    followers = profile.followers.all().select_related('user')

    return render(request, 'users/followers_list.html', {
        'profile_user': profile_user,
        'followers': followers,
        'list_type': 'Followers',
    })


@login_required
def following_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    following = profile.following.all().select_related('user')

    return render(request, 'users/followers_list.html', {
        'profile_user': profile_user,
        'followers': following,
        'list_type': 'Following',
    })