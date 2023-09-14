import django_tables2 as tables
from .models import Forecasts, Players
from django.utils.html import format_html



class UserTable(tables.Table):
    item1 = tables.Column()
    AR = tables.Column()
    ÀR = tables.Column()
    OR = tables.Column()
    VR = tables.Column()


class ItemsTable(tables.Table):
    items = tables.Column(accessor="id")


class ForecastsTable(tables.Table):
    items = tables.Column(accessor="items.id")
    player = tables.Column(accessor="f_email.p_fname")
    nick = tables.Column(accessor="f_email.p_fname")
    forecast = tables.Column(accessor="fvalue1")


    def render_nick(self, value, record):
        return format_html("<b>{} {}</b>", value, record.f_email.p_lname)
    
    def render_forecast(self, value, record):
        return format_html("{}-{}", value, record.fvalue2)


    class Meta:
        model = Forecasts
        fields = ("items", "player", "nick", "forecast")

#    def render_nick()