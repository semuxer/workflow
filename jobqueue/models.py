from django.db import models
from django.db.models import Sum, Min, Max
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz
import datetime
from taggit.managers import TaggableManager

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='Номер телефона', blank=True, max_length=20, help_text='Пример: +38(067) 123-44-55')
    status = models.BooleanField(verbose_name='Доступ', default=True)
    rights = TaggableManager()
    newrights = models.CharField(db_index=True, verbose_name='newrights', null=False, blank=False, default="", max_length=500)
    def addrights(self, *args, **kwargs):
        try:
            nval = str(args[0])
        except:
            return False
        if self.newrights:
            ls = self.newrights.split(",")
        else:
            ls = []
        if nval not in ls:
            ls.append(nval)
            self.newrights = ",".join(ls)
            return True
        else:
            return False

    def delrights(self, *args, **kwargs):
        try:
            nval = str(args[0])
        except:
            return False
        if self.newrights:
            ls = self.newrights.split(",")
        else:
            ls = []
        try:
            ls.remove(nval)
            self.newrights = ",".join(ls)
            return True
        except:
            return False

    def checkrights(self, *args, **kwargs):
        try:
            nval = str(args[0])
        except:
            return False
        if self.newrights:
            ls = self.newrights.split(",")
        else:
            ls = []
        if nval in ls:
            return True
        else:
            return False

    def listrights(self, *args, **kwargs):
        if self.newrights:
            ls = self.newrights.split(",")
        else:
            ls = []
        return ls

    class Meta:
            ordering = ['user']
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Jobs(models.Model):
    customer = models.CharField(db_index=True, verbose_name='Заказчик', null=True, blank=True, default="", max_length=255)
    name = models.CharField(db_index=True, verbose_name='Название работы', default="", max_length=255)
    paper = models.CharField(db_index=True, verbose_name='Бумага', null=True, blank=True, default="", max_length=255)
    info = models.CharField(db_index=True, verbose_name='Дополнительная информация', null=True, blank=True, default="", max_length=255)
    createdatetime = models.DateTimeField(db_index=True, verbose_name='Дата и время создания', default=timezone.now)
    shipmentdatetime = models.DateTimeField(db_index=True, verbose_name='Дата и время отгрузки', default=timezone.now)
    order = models.IntegerField(db_index=True, default=1)
    tags = TaggableManager()
    newtag = models.CharField(db_index=True, verbose_name='newtag', null=False, blank=False, default="", max_length=500)

    color = models.ForeignKey('Colors', verbose_name='Цвет', null=True, blank=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey('Profile',verbose_name='Создал', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        ordering = ['order']

    def addnt(self, *args, **kwargs):
        try:
            nval = str(args[0]).rjust(4,"0")
        except:
            return False
        if self.newtag:
            ls = self.newtag.split(",")
        else:
            ls = []
        if nval not in ls:
            ls.append(nval)
            self.newtag = ",".join(ls)
            return True
        else:
            return False


    def delnt(self, *args, **kwargs):
        try:
            nval = str(args[0]).rjust(4,"0")
        except:
            return False
        if self.newtag:
            ls = self.newtag.split(",")
        else:
            ls = []
        try:
            ls.remove(nval)
            self.newtag = ",".join(ls)
            return True
        except:
            return False

    def checknt(self, *args, **kwargs):
        try:
            nval = str(args[0]).rjust(4,"0")
        except:
            return False        
        if self.newtag:
            ls = self.newtag.split(",")
        else:
            ls = []
        if nval in ls:
            return True
        else:
            return False

    def listnt(self, *args, **kwargs):
        if self.newtag:
            ls = self.newtag.split(",")
        else:
            ls = []
        return ls

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = self.__class__.objects.all().aggregate(largest=Min('order'))['largest']

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
    seton = models.BooleanField(verbose_name='Установить для существующих задач', default=False, help_text='Операция может занять много времени при большом количестве задач в БД.')
    techop = models.BooleanField(verbose_name='Технологическая операция', default=False)
    color = models.ForeignKey('Colors', verbose_name='Цвет', null=True, blank=True, on_delete=models.SET_NULL)
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

class Colors(models.Model):
    name = models.CharField(db_index=True, verbose_name='Название цвета', unique=True, max_length=40)
    text = models.CharField(db_index=True, verbose_name='Цвет текста', default="#000000", max_length=8)
    bg = models.CharField(db_index=True, verbose_name='Цвет фона', default="#FFFFFF", max_length=8)
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
        super(Colors, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
