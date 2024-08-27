from django.db import models
import django_tables2 as tables


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class Dates(models.Model):
    name = models.CharField(max_length=40)
    shift = models.IntegerField()
    round = models.ForeignKey('Rounds', models.DO_NOTHING, blank=True, null=True)
    dia = models.IntegerField(blank=True, null=True)
    competition = models.ForeignKey(Competitions, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dates'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Editions(models.Model):
    competitions = models.ForeignKey(Competitions, models.DO_NOTHING, blank=True, null=True)
    seasons = models.ForeignKey('Seasons', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    code = models.CharField(max_length=4)
    short = models.CharField(max_length=10)
    is_active = models.IntegerField(blank=True, null=True)
    kickoff = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editions'


class Fields(models.Model):
    name = models.CharField(unique=True, max_length=15)
    input = models.CharField(max_length=10)
    nick = models.CharField(unique=True, max_length=1)

    class Meta:
        managed = False
        db_table = 'fields'


class Fixtures(models.Model):
    localteam = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    awayteam = models.ForeignKey('Teams', models.DO_NOTHING, related_name='fixtures_awayteam_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fixtures'


class Forecasts(models.Model):
    items = models.ForeignKey('Items', models.DO_NOTHING, blank=True, null=True)
    f_email = models.CharField(max_length=60, blank=True, null=True)
    ts = models.DateTimeField(blank=True, null=True)
    fvalue1 = models.CharField(max_length=50, blank=True, null=True)
    fvalue2 = models.CharField(max_length=50, blank=True, null=True)
    f1x2 = models.CharField(max_length=1, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    f_isactive = models.IntegerField(blank=True, null=True)
    f_player = models.ForeignKey('Players', models.DO_NOTHING, db_column='f_player', blank=True, null=True)
    f_possible = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forecasts'


class Items(models.Model):
    dates = models.ForeignKey(Dates, models.DO_NOTHING, blank=True, null=True)
    editions = models.ForeignKey('Seasons', models.DO_NOTHING, blank=True, null=True)
    times = models.ForeignKey('Times', models.DO_NOTHING, blank=True, null=True)
    fields = models.ForeignKey(Fields, models.DO_NOTHING, blank=True, null=True)
    fixtures = models.ForeignKey(Fixtures, models.DO_NOTHING, blank=True, null=True)
    scores = models.ForeignKey('Scores', models.DO_NOTHING, blank=True, null=True)
    value1 = models.CharField(max_length=50, blank=True, null=True)
    value2 = models.CharField(max_length=50, blank=True, null=True)
    number_1x2 = models.CharField(db_column='1x2', max_length=1, blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    open = models.DateTimeField(blank=True, null=True)
    close = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    list = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'


class Peoples(models.Model):
    playerdb = models.OneToOneField('Playerdb', models.DO_NOTHING, db_column='playerDB_id', primary_key=True)  # Field name made lowercase. The composite primary key (playerDB_id, communities_id) found, that is not supported. The first column is selected.
    communities = models.ForeignKey(Communities, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'peoples'
        unique_together = (('playerdb', 'communities'),)


class Playerdb(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=60)
    psw = models.CharField(max_length=300)
    stars = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playerDB'


class Players(models.Model):
    playerdb = models.ForeignKey(Playerdb, models.DO_NOTHING, db_column='playerDB_id', blank=True, null=True)  # Field name made lowercase.
    p_fname = models.CharField(max_length=20)
    p_lname = models.CharField(max_length=20)
    p_email = models.CharField(unique=True, max_length=60, blank=True, null=True)
    ppsw = models.CharField(max_length=300, blank=True, null=True)
    paid = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    winnable = models.IntegerField(blank=True, null=True)
    editions = models.ForeignKey(Editions, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'players'


class Rounds(models.Model):
    name = models.CharField(unique=True, max_length=20, blank=True, null=True)
    nick = models.CharField(unique=True, max_length=2, blank=True, null=True)
    stage = models.ForeignKey('Stages', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rounds'


class Scores(models.Model):
    competitions = models.ForeignKey(Competitions, models.DO_NOTHING, blank=True, null=True)
    s_max = models.IntegerField(blank=True, null=True)
    s_low = models.IntegerField(blank=True, null=True)
    s_min = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scores'


class Seasons(models.Model):
    syear = models.TextField(unique=True, blank=True, null=True)  # This field type is a guess.
    season = models.CharField(unique=True, max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seasons'


class Stages(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    nick = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stages'


class Teams(models.Model):
    teamsdb = models.ForeignKey('Teamsdb', models.DO_NOTHING, db_column='teamsDB_id', blank=True, null=True)  # Field name made lowercase.
    editions = models.ForeignKey(Editions, models.DO_NOTHING, blank=True, null=True)
    coef = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    grp = models.CharField(max_length=1, blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    round = models.ForeignKey(Rounds, models.DO_NOTHING, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    rev = models.IntegerField(blank=True, null=True)
    ptsgs = models.DecimalField(db_column='ptsGS', max_digits=6, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ptsko = models.DecimalField(db_column='ptsKO', max_digits=6, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teams'


class Teamsdb(models.Model):
    world_id = models.IntegerField(blank=True, null=True)
    euro_id = models.IntegerField(blank=True, null=True)
    ext_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    ofname = models.CharField(max_length=50, blank=True, null=True)
    short = models.CharField(max_length=20, blank=True, null=True)
    ofshort = models.CharField(max_length=20, blank=True, null=True)
    shield = models.TextField(blank=True, null=True)
    kith = models.TextField(db_column='kitH', blank=True, null=True)  # Field name made lowercase.
    kita = models.TextField(db_column='kitA', blank=True, null=True)  # Field name made lowercase.
    flag = models.TextField(blank=True, null=True)
    ext_coef = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    coef = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    is_club = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    alphabet = models.IntegerField(blank=True, null=True)
    fed = models.TextField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'teamsDB'


class Times(models.Model):
    hores = models.TimeField(unique=True)

    class Meta:
        managed = False
        db_table = 'times'