from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from tinymce import HTMLField


class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug


class Post(models.Model):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )
    PRIVACY_CHOICES = (
        ('Private', 'Private'),
        ('Public', 'Public'),
        ('Friends', 'Friends'),
    )

    # Fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = HTMLField('Content')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Draft', choices=STATUS_CHOICES)
    privacy = models.CharField(max_length=20, default='Private', choices=PRIVACY_CHOICES,
                               help_text='Private - for your eyes only, Friends - visible only to friends, '
                                         'Public - visible to everyone')
    tags = models.ManyToManyField(Tag)

    # Functions
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.status = "Published"
        self.save()

    def __str__(self):
        return self.title
