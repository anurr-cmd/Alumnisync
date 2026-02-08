from django.db import models
from django.contrib.auth.models import User
from urllib.parse import quote_plus
from django.utils.text import slugify

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('alumni', 'Alumni'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    roll_no = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    passout_year = models.IntegerField(blank=True, null=True)
    current_status = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    image_url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,      # 👈 IMPORTANT (temporary)
        blank=True
    )
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        title_lower = self.title.lower()

        if "job" in title_lower:
            self.image_url = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
        elif "tech" in title_lower or "ai" in title_lower:
            self.image_url = "https://images.unsplash.com/photo-1519389950473-47ba0277781c"
        elif "alumni" in title_lower or "meet" in title_lower:
            self.image_url = "https://images.unsplash.com/photo-1523580494863-6f3031224c94"
        elif "sports" in title_lower:
            self.image_url = "https://images.unsplash.com/photo-1508609349937-5ec4ae374ebf"
        elif "startup" in title_lower:
            self.image_url = "https://images.unsplash.com/photo-1559136555-9303baea8ebd"
    
        super().save(*args, **kwargs)


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    posted_on = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.image_url:
            query = slugify(self.title)
            self.image_url = f"https://source.unsplash.com/600x400/?job,career,{query}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# 🔹 ANNOUNCEMENT
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    image_url = models.URLField(blank=True)
    posted_on = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.image_url or self.image_url.strip() == "":
            self.image_url = "https://img.freepik.com/premium-vector/megaphone-with-announcement-speech-bubble-banner-loudspeaker_1027249-725.jpg"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title