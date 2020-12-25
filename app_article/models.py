import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Token(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4(), editable=False)
    is_expired = models.BooleanField(default=False)


class ArticleModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=4, choices=(
        ('arch', 'Architecture'),
        ('news','News'),
        ('heal', 'Health')
    ))
    title = models.CharField(max_length=500)
    data = models.TextField(max_length=1000,blank=True,null=True)
    created_on = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    # def get_absolute_url(self):
    #     return reverse("article:article-detail", kwargs={"pk": self.pk})

    def publish(self):
        self.published_date = timezone.now()
        self.save()



    def __str__(self):
        return self.title



