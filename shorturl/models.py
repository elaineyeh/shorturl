from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User


class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    url = models.TextField()
    code = models.CharField(max_length=64, blank=True, unique=True)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.code == '':
            while True:
                self.code = get_random_string(length=8)
                if not Url.objects.filter(code=self.code):
                    break

        super(Url, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '{} -> {}'.format(self.url, self.code)