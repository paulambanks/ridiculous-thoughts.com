from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from tinymce import HTMLField
from django.utils import timezone

from accounts.models import CustomUser


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = HTMLField('Content')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Draft', choices=STATUS_CHOICES)
    privacy = models.CharField(max_length=20, default='Private', choices=PRIVACY_CHOICES,
                               help_text='Private - for your eyes only, Friends - visible only to friends, '
                                         'Public - visible to everyone')
    tags = models.ManyToManyField(Tag, blank=True, through='TaggedPost')
    sharing = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through='SharedPost')

    # Functions
    def save(self, *args, **kwargs):
        self.slug = '%s-%s' % (slugify(self.title), str(self.id))
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.status = "Published"
        self.published = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class SharedPost(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shared_post_id")
    user = models.ForeignKey(CustomUser, default='', on_delete=models.CASCADE, related_name="user_id",
                             help_text="Just do not share the post with yourself!")

    def __unicode__(self):
        return self.id

    class Meta:
        unique_together = ('post', 'user')

    def save(self, *args, **kwargs):
        super(SharedPost, self).save(*args, **kwargs)


class TaggedPost(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tagged_post_id")
    tag = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE, related_name="tag_id")

    class Meta:
        unique_together = ('post', 'tag')

    def __str__(self):
        return self.tag
