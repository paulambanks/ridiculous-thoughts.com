from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, UserProfile
from django.utils.crypto import get_random_string


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    form = UserProfileForm


class CustomUserAdmin(UserAdmin):
    """
    A UserAdmin that sends a password-reset email when creating a new user,
    unless a password was entered.
    """

    add_form = CustomUserCreationForm
    inlines = [UserProfileInline]
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address and click save."
                " The user will be emailed a link allowing them to login to"
                " the site and set their password."
            ),
            'fields': ('email', 'username', 'first_name', 'last_name'),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change and (not form.cleaned_data['password1'] or not obj.has_usable_password()):
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                subject_template_name='registration/account_creation_subject.txt',
                email_template_name='registration/account_creation_email.html',
            )
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name',)


admin.site.register(CustomUser, CustomUserAdmin)



