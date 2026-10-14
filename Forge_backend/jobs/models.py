from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Job(models.Model):
    class EmployementType(models.TextChoices):
        FULL_TIME = "full_time","Full-time"
        PART_TIME = "part_time","Part-time"
        CONTRACT = "contract","Contract"
        INTERNSHIP = "internship","Internship"
        FREELANCE = "freelance","Freelance"

    class WorkPlace(models.TextChoices):
        ONSITE = "onsite","On-site"
        REMOTE = "remote","Remote"
        HYBRID = "hybrid","Hybrid"

    class ExperienceLevel(models.TextChoices):
        ENTRY = "entry","Entry-level"
        JUNIOR = "junior","Junior"
        MID = "mid","Mid-level"
        SENIOR = "senior","Senior"
        LEAD = "lead","Lead"

    company = models.ForeignKey(
        "companies.company",
        on_delete=models.PROTECT,
        related_name="jobs"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220,unique=True)

    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)

    employment_type = models.CharField(
        max_length=20,
        choices=EmployementType.choices,
    )

    workplace_type = models.CharField(
        max_length=30,
        choices= WorkPlace.choices,
        default= WorkPlace.ONSITE,
    )

    experience_level = models.CharField(
        max_length=30,
        choices= ExperienceLevel.choices,
        default= ExperienceLevel.ENTRY,
    )

    location = models.CharField(max_length=200,blank=True)
    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank = True,
        validators=[MinValueValidator(0)],
    )
    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    salary_currency = models.CharField(
        max_length=3,
        default="NPR",
    )
    application_deadline = models.DateField(
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields = ["is_published","-created_at"],
                name="job_pub_created_indx"
            ),
            models.Index(
                fields = ["company","-created_at"],
                name="job_company_created_indx"
            )               
        ]
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "job"
            slug = base_slug
            counter = 2

            while Job.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.company.name}"
