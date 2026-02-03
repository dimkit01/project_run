from email.policy import default

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Run(models.Model):
    RUN_STATUS_CHOICES = {
        ('init', 'Забег инициализирован'),
        ('in_progress', 'Забег начат'),
        ('finished', 'Забег закончен'),
    }

    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=RUN_STATUS_CHOICES, default='init')


class AthleteInfo(models.Model):

    weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(900)])
    goal = models.TextField()
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
