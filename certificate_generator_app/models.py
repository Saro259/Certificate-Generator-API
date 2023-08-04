from django.db import models
import uuid

# Create your models here.

class Certificate(models.Model):
    certificate_unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    certificate_generation_date = models.DateField(auto_now_add=True)
    

class CertificateDetails(models.Model):
    certificate_id = models.ForeignKey(Certificate, on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    certificate_award_date = models.DateField()



