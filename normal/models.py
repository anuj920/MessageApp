from django.db import models
from django.urls import reverse

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title= models.CharField(max_length = 200)
    msg= models.TextField(max_length = 99999)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('message_detail',kwargs={'pk':self.pk})