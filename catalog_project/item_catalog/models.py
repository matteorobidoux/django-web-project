from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

TYPE_CHOICES = (
    ('practical', 'PRACTICAL'),
    ('theoretical', 'THEORETICAL'),
    ('fundamental research', 'FUNDAMENTAL RESEARCH'),
    ('imperical', 'IMPERICAL')
)

STATUS_CHOICES = (
    ('completed', 'COMPLETED'),
    ('ongoing', 'ONGOING'),
    ('planned', 'PLANNED')
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
    rate = models.DecimalField(default=0.0, decimal_places=1, max_digits=3, validators=[
        MaxValueValidator(5.0),
        MinValueValidator(0.0)
    ])
    snapshot = models.ImageField(default='default.jpg', upload_to='project_photos')
    likes = models.ManyToManyField(User, related_name='item_likes', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_keywords(self):
        new_keywords = ""
        for keyword in self.keyword_list.split(","):
            new_keyword = "#" + keyword
            new_keywords += new_keyword + " "
        return new_keywords

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

        img = Image.open(self.snapshot.path)
        
        if img.height > 400 or img.width > 400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save(self.snapshot.path)

class Comment(models.Model):
    content = models.TextField(max_length=300)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="comments", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)