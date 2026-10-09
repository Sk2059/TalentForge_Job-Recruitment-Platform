from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.conf import settings
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    """Custom user model to extend the default user model
    using email as the unique identifier instead of username.
    """
    username = None
    email = models.EmailField(unique=True,db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    
    def __str__(self):
        return self.email

class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )

    profile_image = models.ImageField(
        upload_to="profile_images/candidates/",
        blank=True,
        null=True,
    )
    phone = models.CharField(max_length=20,blank=True)
    location = models.CharField(max_length=150,blank=True)
    headline = models.CharField(max_length=200,blank=True)
    bio = models.TextField(blank=True)

    skills = models.JSONField(default=list,blank=True)
    experience = models.JSONField(default=list,blank=True)
    education = models.JSONField(default=list,blank=True)

    resume = models.FileField(
        upload_to="candidate_resume/",
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf","doc","docx"]
            )
        ],
    )
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"candidate profile : {self.user.email}"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruiter_profile",
    )

    profile_image = models.ImageField(
        upload_to="Profile_images/Recruiters/",
        blank=True,
        null=True,
    )

    job_title = models.CharField(max_length=150,blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20,blank=True)

    is_varified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recruiter profile: {self.user.email}"