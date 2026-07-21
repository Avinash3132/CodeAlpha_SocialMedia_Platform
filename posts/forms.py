from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'post-content',
            'placeholder': "What's on your mind?",
            'rows': 3,
            'style': 'resize:none; border:none; outline:none; '
                     'width:100%; font-size:1rem; background:transparent;',
            'maxlength': 500,
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'style': 'display:none;',
            'id': 'post-image-input',
        })
    )

    class Meta:
        model = Post
        fields = ['content', 'image']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        if not content and not image:
            raise forms.ValidationError(
                'Post must have either text or an image.'
            )
        return cleaned_data


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Write a comment...',
            'class': 'form-control',
            'style': 'border-radius:50px;',
        })
    )

    class Meta:
        model = Comment
        fields = ['content']