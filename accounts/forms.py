from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserProfile
from django import forms


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150, help_text='Required')
    first_name = forms.CharField(max_length=20, help_text='Required')
    last_name = forms.CharField(max_length=20, help_text='Required')
    """
    A UserCreationForm with optional password inputs.
    """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, the 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',)


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.empty_permitted = False # Here

    class Meta:
        model = UserProfile
        fields = ('bio', 'country', 'city', 'avatar',)

# ---------------USER PROFILE------------------------







