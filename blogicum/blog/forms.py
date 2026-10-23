from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and editing publications."""

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'image',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
            ),
        }


class CommentForm(forms.ModelForm):
    """Form for commenting posts"""

    class Meta:
        model = Comment
        fields = ('text',)
