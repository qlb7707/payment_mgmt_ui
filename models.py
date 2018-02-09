# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DailyStastics(models.Model):
    year = models.IntegerField(primary_key=True)
    month = models.SmallIntegerField()
    cost = models.FloatField()
    user = models.ForeignKey('UserInfo', models.DO_NOTHING)
    day = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'daily_stastics'
        unique_together = (('year', 'month', 'day'),)


class Payment(models.Model):
    user_id = models.SmallIntegerField()
    time = models.IntegerField()
    cost = models.FloatField()
    pri_type = models.SmallIntegerField()
    sec_type = models.SmallIntegerField()
    period = models.SmallIntegerField()
    cost_name = models.CharField(max_length=256)
    seller = models.CharField(max_length=128)
    year = models.IntegerField()
    mon = models.SmallIntegerField()
    day = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'payment'


class PeriodTbl(models.Model):
    value = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'period_tbl'


class PriTypeTbl(models.Model):
    value = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'pri_type_tbl'


class SecTypeTbl(models.Model):
    value = models.SmallIntegerField(primary_key=True)
    pri_type = models.SmallIntegerField()
    description = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'sec_type_tbl'


class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'user_info'
