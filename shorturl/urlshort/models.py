from django.db import models
import random
import string
# Create your models here.
class UrlData(models.Model):

    url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        # return f"your url was: {self.url}, shortened is: {self.short_url}"
        return self.url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.short_url = self.gen_short_url()
        return super().save(*args, **kwargs)
        
    def gen_short_url(self):
        chars = string.ascii_letters
        short_url = ' '.join(random.choice(chars)for _ in range(6))

        return short_url