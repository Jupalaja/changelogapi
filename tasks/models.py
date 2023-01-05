from helpers.models import TrackingModel
from django.db import models
from authentication.models import User


class Task(TrackingModel):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    creator_id = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
