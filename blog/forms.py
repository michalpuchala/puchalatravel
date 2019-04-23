from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class LanguageChangeForm(forms.Form):
    language = forms.CharField(max_length=10)

    class Meta:
        fields = ('language',)
