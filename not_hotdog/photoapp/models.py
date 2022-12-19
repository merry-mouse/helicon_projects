from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from api.send import send_message


class Photo(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = TaggableManager(blank=True) 
    not_hotdog_flag = models.BooleanField(null=True) # if not a hotdog = True


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        pk = self.pk
        photo = super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        if pk is None:
            send_message("New image uploaded", {
                "id": self.pk,
                "title": self.title,
                "not_hotdog_flag": self.not_hotdog_flag,
                "image": self.image.path,
            })
        return photo
