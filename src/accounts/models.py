from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # First/last name is not a global-friendly pattern
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Email & Password are required by default.

    def __str__(self):
        return str(self.email)

    objects = UserManager()


# class Country(models.Model):
#     pass
#
#
# class City(models.Model):
#     pass


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True,
        verbose_name='Member profile')
    bio = models.TextField(
        max_length=250,
        blank=True,
        default='',
        help_text="Maximum 250 characters ",
    )
    avatar = models.ImageField(
        upload_to='uploads/',
        blank=True,
        default='static/images/crazycat.jpeg',
        verbose_name="Your Current Profile Avatar"
    )
    country = models.CharField(
        max_length=100,
        default='',
        blank=True
    )
    city = models.CharField(
        max_length=100,
        default='',
        blank=True
    )

    def __str__(self):
        return str(self.user)

    @property
    def get_absolute_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return "{0}{1}".format(settings.MEDIA_URL, self.avatar.url)
        else:
            return '/static/crazycat.jpeg'


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=CustomUser)



