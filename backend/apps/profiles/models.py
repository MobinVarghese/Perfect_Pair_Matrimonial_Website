from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Profile(models.Model):
    """User Profile model for matrimonial website."""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    RELIGION_CHOICES = [
        ('hindu', 'Hindu'),
        ('muslim', 'Muslim'),
        ('christian', 'Christian'),
        ('sikh', 'Sikh'),
        ('buddhist', 'Buddhist'),
        ('jain', 'Jain'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    name = models.CharField(max_length=255, help_text='Full name')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True, help_text='Date of birth (must be 18+ years old)')
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        help_text='Age in years (calculated from date of birth)'
    )
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True, default='')
    occupation = models.CharField(max_length=255, blank=True)
    education = models.CharField(max_length=255, blank=True)
    height = models.DecimalField(
        max_digits=4, decimal_places=2,
        help_text='Height in feet (e.g., 5.6)', null=True, blank=True
    )
    location = models.CharField(max_length=255, help_text='City, State, Country')
    about = models.TextField(blank=True, help_text='About yourself')
    desired_partner_traits = models.TextField(blank=True, help_text='Desired partner characteristics')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, help_text='Profile photo')
    mobile_number = models.CharField(max_length=15, unique=True, help_text='Mobile number with country code')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']

    def calculate_age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or \
               (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return self.age

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            self.age = self.calculate_age()
        if self.gender:
            self.gender = self.gender.lower()
        if self.name:
            self.name = self.name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}'s Profile ({self.user.username})"
