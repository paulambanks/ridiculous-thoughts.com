from django import forms
from .models import Post, TagPost
from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class TagPostForm(forms.ModelForm):

    class Meta:
        model = TagPost
        fields = ('tagged_with', )


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': True, 'cols': 80, 'rows': 30}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'privacy',)


class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(required=True)
    email = forms.CharField(required=False)

