from django.db import models

# Create your models here.
from django.db import models

class SsqOtherPredict(models.Model):
    issueNumber = models.CharField(max_length=50, primary_key=True)
    result = models.TextField()

    def __str__(self):
        return self.issueNumber