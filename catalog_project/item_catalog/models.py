import math
import uuid
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

TYPE_CHOICES = (
    ('Practical', 'PRACTICAL'),
    ('Theoretical', 'THEORETICAL'),
    ('Fundamental research', 'FUNDAMENTAL RESEARCH'),
    ('Empirical', 'Empirical')
)

STATUS_CHOICES = (
    ('Completed', 'COMPLETED'),
    ('Ongoing', 'ONGOING'),
    ('Planned', 'PLANNED')
)

class Item(models.Model):
    # Define the class for permissions
    class Meta:
        permissions = (
            ("delete_user_item", "Delete own item"),
            ("change_user_item", "Change own item"),
            ("rate_item", "Rate item"),
        )

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='practical')
    field = models.CharField(max_length=100)
    keyword_list = models.CharField(max_length=200, verbose_name='Keyword List (Seperate with commas)')
    content = models.TextField()
    url = models.URLField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='planned')
    snapshot = models.ImageField(default='default.jpg', upload_to='project_photos')
    likes = models.ManyToManyField(User, related_name='item_likes', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    flagged = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Reduce image resolution
        save_thumbnail_image(self.snapshot)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_keywords(self):
        return self.keyword_list.split(",")

    def total_likes(self):
        return self.likes.count()

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(item=self)
        for rating in ratings:
            sum += rating.rate

        if len(ratings) > 0:
            return math.floor(sum / len(ratings)*100)/100
        else:
            return 0.0

    def latest_flag(self):
        flag = self.flag_item_target.order_by('-timestamp')[0]
        return flag


class Comment(models.Model):
    content = models.TextField(max_length=300)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="comments", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.FloatField(
        validators=[MinValueValidator(0.0),MaxValueValidator(5.0)],
    )


class ItemFlag(models.Model):
    item = models.ForeignKey(Item, models.CASCADE, related_name='flag_item_target')
    timestamp = models.DateTimeField(auto_now_add=True)
    blame = models.ForeignKey(User, models.CASCADE, related_name='flag_item_flag')

    def __str__(self):
        return f"{self.item.name} flagged on {self.timestamp}"


def save_thumbnail_image(image_field):
    img = Image.open(BytesIO(image_field.read()))
    # Convert to RGBA format
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    if img.height > 400 or img.width > 400:
        # limit the image size
        output_size = (400, 400)
        img.thumbnail(output_size, Image.ANTIALIAS)
        filename = image_field.name.split('.')[0]+uuid.uuid4().hex

        # create a bytesIO output
        image_output_buffer = BytesIO()
        img.save(image_output_buffer, format="PNG", quality=70)
        image_output_buffer.seek(0)
        # Make a file
        image_field.save(filename + ".png", ContentFile(image_output_buffer.getvalue()), save=False)