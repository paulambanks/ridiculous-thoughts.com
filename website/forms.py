from django import forms
from .models import Post, TaggedPost, SharedPost
from accounts.models import CustomUser
from tinymce.widgets import TinyMCE
from django.forms.models import inlineformset_factory


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'privacy',)
        widgets = {
            'content': TinyMCE(attrs={
                'required': True,
                'cols': 80,
                'rows': 30,
                'placeholder': 'Write some of your Ridiculous Thoughts!',
            }),
            'title': forms.TextInput(attrs={
                'required': True,
                'cols': 80,
                'placeholder': 'Give your Post the title',
            }
            )
        }


class TagPostForm(forms.ModelForm):

    class Meta:
        model = TaggedPost
        fields = ('tag', )


class SharedPostForm(forms.ModelForm):
    """ request user excluded """

    class Meta:
        model = SharedPost
        fields = ('user',)
        user = forms.ModelChoiceField(queryset=CustomUser.objects.all())


class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(required=False)
    email = forms.CharField(required=False)

