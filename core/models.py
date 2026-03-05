from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import re
from urllib.parse import urlparse, parse_qs

class Teaching(models.Model):
    CATEGORY_CHOICES = [
        ('quran', 'Qur’an'),
        ('hadith', 'Hadith'),
        ('fiqh', 'Fiqh'),
        ('reminder', 'Reminder'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='teachings/', blank=True, null=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('graphic', 'Graphic'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    image = models.ImageField(upload_to='media/images/', blank=True, null=True)
    audio_file = models.FileField(upload_to='media/audio/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)

    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Media.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


    def get_youtube_id(self):
        if not self.youtube_url:
            return None

        url = self.youtube_url

        # Case 1: youtu.be short link
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]

        # Case 2: normal youtube link
        if "youtube.com" in url:
            parsed = urlparse(url)
            return parse_qs(parsed.query).get("v", [None])[0]

        return None

class Event(models.Model):
    title = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True
    )

    description = models.TextField()

    location = models.CharField(
        max_length=200,
        blank=True
    )

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    registration_url = models.URLField(blank=True)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if timezone.is_naive(self.start_date):
            self.start_date = timezone.make_aware(self.start_date, timezone.get_current_timezone())
        super().save(*args, **kwargs)


class CommunityPost(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

from django.utils.text import slugify

slug = models.SlugField(unique=True, blank=True)

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
