from django import forms

from blog.models import Post


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
