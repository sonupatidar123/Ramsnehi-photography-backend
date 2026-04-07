from django.db import models
from cloudinary.models import CloudinaryField
import re

# ---------------------------------------------------------------------------
# 1. GALLERY MODEL
# ---------------------------------------------------------------------------

class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('Pre-Wedding', 'Pre-Wedding'),
        ('Wedding', 'Wedding'),
        ('Maternity', 'Maternity'),
        ('Newborn', 'Newborn'),
        ('Toddler', 'Toddler'),
    ]

    title = models.CharField(max_length=255)
    image = CloudinaryField('image')  
    
    # db_index add kiya: Category filter 10x fast ho jayega
    category = models.CharField(
        max_length=100, 
        choices=CATEGORY_CHOICES, 
        db_index=True 
    )
    
    # db_index add kiya: "Newest First" sorting instant ho jayegi
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.category})"
# ---------------------------------------------------------------------------
# 2. FILM / VIDEO MODEL
# ---------------------------------------------------------------------------
class Film(models.Model):
    TYPE_CHOICES = [
        ('Cinematic Film', 'Cinematic Film'),
        ('Viral Reel', 'Viral Reel'),
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    # video_id stores the 11-character YouTube ID
    video_id = models.CharField(
        max_length=200, 
        help_text='Enter YouTube Video ID or the full YouTube URL'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.type})"

    def extract_video_id(self, value):
        """
        Regex to pull the 11-char ID from any standard YouTube URL
        """
        pattern = r'(?:v=|\/|embed\/|youtu.be\/)([0-9A-Za-z_-]{11})'
        match = re.search(pattern, value)
        return match.group(1) if match else value

    def save(self, *args, **kwargs):
        # Automatically clean the URL into an ID before saving to DB
        if self.video_id:
            self.video_id = self.extract_video_id(self.video_id)
        super().save(*args, **kwargs)

    @property
    def thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.video_id}/maxresdefault.jpg"


# ---------------------------------------------------------------------------
# 3. TESTIMONIAL MODEL
# ---------------------------------------------------------------------------
class Testimonial(models.Model):
    client_name = models.CharField(max_length=255)
    text = models.TextField()
    # This matches React's formData.append('client_image', ...)
    client_image = CloudinaryField('image', blank=True, null=True) 
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"Testimonial by {self.client_name}"


# ---------------------------------------------------------------------------
# 4. INQUIRY MODEL
# ---------------------------------------------------------------------------
class Inquiry(models.Model):
    INQUIRY_TYPE_CHOICES = [
        ('Wedding Photography', 'Wedding Photography'),
        ('Pre-Wedding Shoot', 'Pre-Wedding Shoot'),
        ('Films & Cinematography', 'Films & Cinematography'),
        ('Commercial/Event', 'Commercial/Event'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20, blank=True, null=True) 
    inquiry_type = models.CharField(max_length=100, choices=INQUIRY_TYPE_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        # FIXED: Removed reference to 'event_date' to prevent 500 errors
        return f"{self.full_name} — {self.inquiry_type} ({self.submitted_at.strftime('%d %b %Y')})"