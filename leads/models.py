from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Lead(models.Model):
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey(
        "Agent",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        "Category",
        related_name="leads",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    profile_picture = models.ImageField(blank=True, null=True, upload_to="profile_pictures/")
    converted_date = models.DateTimeField(blank=True, null=True)
    # objects = LeadManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def handle_upload_follow_ups(instance, filename):
    return f"leads_followups/lead_{instance.lead.pk}/{filename}"


class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups" ,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.first_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30) # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
