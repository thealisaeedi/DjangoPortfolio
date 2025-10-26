from django import forms
from .models import Comment

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Your Message", "rows": 5}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

        