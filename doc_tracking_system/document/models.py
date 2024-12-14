from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Document(models.Model):
    CATEGORY_CHOICES = [('Finance', 'Finance'), ('HR', 'HR'), ('Legal', 'Legal')]
    SENSITIVITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    VISIBILITY_CHOICES = [('Private', 'Private'), ('Department', 'Department'), ('Company-wide', 'Company-wide')]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    sensitivity = models.CharField(max_length=50, choices=SENSITIVITY_CHOICES)
    visibility = models.CharField(max_length=50, choices=VISIBILITY_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    forwarded_to = models.ForeignKey('users.Department', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class DocumentStatus(models.Model):
    STATUS_CHOICES = [
        ('In Process', 'In Process'),
        ('Forwarded', 'Forwarded'),
        ('Returned', 'Returned'),
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Released', 'Released'),
    ]

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
