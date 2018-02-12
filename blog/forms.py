from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


    title = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'autofocus': True, 'autocapitalize': 'on','type': 'text'})
    )

    text = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'autofocus': True,'autocapitalize':'off', 'type':'text'}))