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
    distance = models.FloatField(default=0.0)


class AthleteInfo(models.Model):

    weight = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(899)])
    goal = models.TextField()
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)


class Challenge(models.Model):
    full_name = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)


class Positions(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=8,  decimal_places=4, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    
    
class CollectibleItem(models.Model):
    name = models.CharField(max_length=255)
    uid = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=8,  decimal_places=4, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    picture = models.URLField()
    value = models.IntegerField()