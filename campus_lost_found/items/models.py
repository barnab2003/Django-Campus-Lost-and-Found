from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    STATUS_CHOICES = (
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('CLAIMED', 'Claimed')
    )
    
    CATEGORY_CHOICES = (
        ('ELECTRONICS', 'Electronics'),
        ('BOOKS', 'Books & Notebooks'),
        ('ID_CARD', 'ID Cards & Wallets'),
        ('OTHER', 'Other')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='LOST')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    location = models.CharField(max_length=255, help_text="Where was it lost or found?")
    date_reported = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    
    # Links the item to the student who reported it
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_email = models.EmailField()

    def __str__(self):
        return f"{self.status}: {self.title}"