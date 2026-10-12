from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Company(models.Model):
    class CompanySize(models.TextChoices):
        STARTUP = "startup","Startup (1-10)"
        SMALL = "small","Small (11-50)"
        MEDIUM = "medium","Medium (51-200)"
        LARGE = "large","large (201-1000)"
        ENTERPRISE = "enterprise" "Enterprise (1000+)"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.PROTECT,
        related_name="owned_companies"
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220,unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200,blank=True)
    industry = models.CharField(max_length=100,blank=True)
    company_size = models.CharField(
        max_length=50,
        choices=CompanySize.choices,
        blank=True
    )
    is_varified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self,*args,**kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "comapny"
            slug = base_slug
            counter = 2

            while Company.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super.save(*args,**kwargs)

    def __str__(self):
        return self.name