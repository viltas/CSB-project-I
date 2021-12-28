from django.db import models
import datetime
from django.utils import timezone

class Lunch(models.Model):
    class Meta:
        verbose_name_plural = "lunches"
    lunch = models.CharField(max_length=200)
    date = models.DateField('date', unique=True)
    def __str__(self):
        return self.lunch
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now     

class Choice(models.Model):
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice

       