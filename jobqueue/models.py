from django.db import models
from django.db.models import Sum, Min, Max
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz
import datetime
from taggit.managers import TaggableManager

# Create your models here.
class Jobs(models.Model):
    name = models.CharField(db_index=True, verbose_name='Название работы', default="", max_length=128)
    createdatetime = models.DateTimeField(db_index=True, verbose_name='Дата и время создания', default=timezone.now)
    shipmentdatetime = models.DateTimeField(db_index=True, verbose_name='Дата и время отгрузки', default=timezone.now)
    order = models.IntegerField(db_index=True, default=1)
    tags = TaggableManager()
    class Meta:
        ordering = ['order']
    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = self.__class__.objects.all().aggregate(largest=Max('order'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order = last_id + 1
        super(Jobs, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Tagtype(models.Model):
    name = models.CharField(db_index=True, verbose_name='Название тега', unique=True, max_length=100)
    icon2 = models.CharField(db_index=True, verbose_name='Иконка', max_length=100, null=True, blank=True)
    #icon = models.CharField(db_index=True, verbose_name='Иконка', max_length=100, null=True,blank=True,default="")
    order = models.IntegerField(db_index=True, default=0)
    class Meta:
        ordering = ['order']
    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = self.__class__.objects.all().aggregate(largest=Max('order'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.order = last_id + 1
        super(Tagtype, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
