from django import forms
from .models import Post
from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': True, 'cols': 80, 'rows': 30}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'tags',)


class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
