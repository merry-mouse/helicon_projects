from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


class Photo(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = TaggableManager(blank=True) 
    hotdog_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if 'hotdog' in self.title.lower():
            self.hotdog_flag = True
        return super(Photo, self).save(*args, **kwargs)


