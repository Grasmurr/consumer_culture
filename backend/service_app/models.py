from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_preparing_date = models.DateField(null=True) #начало работы по подготовке мероприятия
    start_event_date = models.DateField(null=True)  # начало работы на площадке
    finish_event_date = models.DateField(null=True)  # конец работы на площадке


# class Event(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     price_for_new = models.IntegerField()
#     price_for_old = models.IntegerField()
#     event_photo_id = models.CharField(max_length=50)
#     ticket_photo_id = models.CharField(max_length=50)
#     description = models.TextField()
#     event_date = models.DateField(null=True)
#
#
# class MemberGirl(models.Model):
#     telegram_id = models.BigIntegerField(null=True)
#     full_name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     unique_id = models.CharField(max_length=50)
#     discussion_topics = models.TextField()
#     joining_purpose = models.TextField()
#
#
# class Newsletter(models.Model):
#     number = models.IntegerField(null=True)
#     photo_id = models.TextField()
#     text = models.TextField()
