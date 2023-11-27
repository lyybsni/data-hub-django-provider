from django.db import models
from django.utils import timezone


class Applicant(models.Model):
    applicant_id = models.CharField(max_length=10)
    applicant_name = models.CharField(max_length=25)
    phone_number = models.BigIntegerField(null=True)
    graduate_date = models.DateField(null=True)

    update_date = models.DateField(null=True, default=timezone.now)

    def __str__(self):
        return self.applicant_id
