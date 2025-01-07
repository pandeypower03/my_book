from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class CustomUser(AbstractUser):
    # Additional fields for custom user model
   
    birth_year = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    public_visibility = models.BooleanField(default=True)

    # Calculated field for age based on birth_year
    def calculate_age(self):
        current_year = datetime.now().year
        if self.birth_year:
            return current_year - self.birth_year
        return None

    def __str__(self):
        return self.username
    
class UploadedFiles(models.Model):
    book_title = models.CharField(max_length=100)
    book_description = models.TextField()
    visibility = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')])
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_of_published = models.PositiveIntegerField()
    file_upload = models.FileField(upload_to='news/', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Nullable field
    def __str__(self):
        return self.book_title
