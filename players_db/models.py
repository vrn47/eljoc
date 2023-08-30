from django.db import models

# Create your models here.

class PlayerDB(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=60)
    psw = models.CharField(max_length=300)
    stars = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playerDB'

class Players(models.Model):
    playerdb = models.ForeignKey(PlayerDB, models.DO_NOTHING, db_column='playerDB_id', blank=True, null=True)  # Field name made lowercase.
    p_fname = models.CharField(max_length=20)
    p_lname = models.CharField(max_length=20)
    p_email = models.CharField(unique=True, max_length=60, blank=True, null=True)
    ppsw = models.CharField(max_length=300, blank=True, null=True)
    paid = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    winnable = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'players'

class Communities(models.Model):
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'communities'


class Competitions(models.Model):
    name = models.CharField(unique=True, max_length=25, blank=True, null=True)
    period = models.IntegerField()
    start = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'competitions'


class Seasons(models.Model):
    syear = models.TextField(unique=True, blank=True, null=True)  # This field type is a guess.
    season = models.CharField(unique=True, max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seasons'


class Editions(models.Model):
    competitions = models.ForeignKey(Competitions, models.DO_NOTHING, blank=True, null=True)
    seasons = models.ForeignKey('Seasons', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    code = models.CharField(max_length=4)
    short = models.CharField(max_length=10)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editions'