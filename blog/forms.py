from django import forms

from .models import Post, CATEGORY_CHOICES, Comment



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'category')
    category=forms.Select(choices=CATEGORY_CHOICES)
    title = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'autofocus': True, 'autocapitalize': 'on','type': 'text'})
    )

    text = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'autofocus': True,'autocapitalize':'off', 'type':'text'}))

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)