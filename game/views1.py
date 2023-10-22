from django.shortcuts import render, redirect, HttpResponse
from .models import Items, Fixtures, Teams, Teamsdb, Forecasts, Players, Scores, Dates, Rounds, Stages, Communities, Editions, Dates
from .tables import ForecastsTable, UserTable, ItemsTable
from .forms import ItemsForm, ForecastsForm, PlayersForm
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.db.models import Sum, Count, TextField, Q, F, Max, Min, Avg, Func, Window
from django.db.models.functions import Cast, Rank, DenseRank, ExtractYear
from array import *
import numpy as np

import requests
import json
import django_tables2 as tables
import datetime


# Create your views here.

def game(request):
        
    print('Game')
    
    data = Items.objects.filter(editions=33, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    print('data', data-38)
    items = Forecasts.objects.filter(items__editions=33, f_isactive=1, ts__lte=timezone.now())
    stnd = items.values('f_email').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        w=F('f_email__winnable'),
        p=F('f_email__paid'),
        stars=F('f_email__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates=data)),
        dlt2=Sum(('points'),filter=Q(items__dates=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
    ).order_by('-tot', '-tot2', '-fn')
    print('stnd', stnd)
    stnd5 = stnd[:5]
    stats = stnd.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
    )
    print('stats', stats)
    
    return render(request, 'game.html', {
            'standings': stnd5,
            'stats': stats,
            'data': data-38,
        })

def items(request):        
    item = Items.objects.all()
    fixture = Fixtures.objects.all()
    team = Teams.objects.all()
    teamdb = Teamsdb.objects.all()
    item1 = Items.objects.get(id=1)
#    iteminfo = Playerdb.objects.get(id=pid)
    form = ItemsForm

    return render(request, 'items.html', {
        'item': item,
        'fixture': fixture,
        'team': team,
        'teamdb': teamdb,
        'form': form,
    })

def forecasts(request):
    time = timezone.now()
    print(time)    
    item = Items.objects.filter(open__lt=time,close__gt=time, ).exclude(fields_id=1).exclude(fields_id=6)
    fixture = Fixtures.objects.all()
    team = Teams.objects.filter(editions=33).order_by('coef')
    team_3 = Teams.objects.filter(editions=33).order_by('-coef')
    team_A = Teams.objects.filter(editions=33, grp='A').order_by('pos')
    team_B = Teams.objects.filter(editions=33, grp='B').order_by('pos')
    team_C = Teams.objects.filter(editions=33, grp='C').order_by('pos')
    team_D = Teams.objects.filter(editions=33, grp='D').order_by('pos')
    team_E = Teams.objects.filter(editions=33, grp='E').order_by('pos')
    team_F = Teams.objects.filter(editions=33, grp='F').order_by('pos')
    team_G = Teams.objects.filter(editions=33, grp='G').order_by('pos')
    team_H = Teams.objects.filter(editions=33, grp='H').order_by('pos')
    team_rev = Teams.objects.filter(editions=33, rev=1).order_by('-coef')
    teamdb = Teamsdb.objects.all()
    teamdb_20 = Teamsdb.objects.filter()
    teamdb_EN = Teamsdb.objects.filter(fed='ENG').order_by('id')
    teamdb_ES = Teamsdb.objects.filter(fed='ESP').order_by('id')
    teamdb_IT = Teamsdb.objects.filter(fed='ITA').order_by('id')
    teamdb_DE = Teamsdb.objects.filter(fed='DEU').order_by('id')
    teamdb_FR = Teamsdb.objects.filter(fed='FRA').order_by('id')
    teamdb_PT = Teamsdb.objects.filter(fed='POR').order_by('id')
    teamdb_ND = Teamsdb.objects.filter(fed='NED').order_by('id')

    forecast = Forecasts.objects.all()
    form = ForecastsForm
    form2 = PlayersForm

    if request.method == 'GET':
        print('enviando formulario forecast')
        return render(request, 'forecasts.html', {
            'forecast': forecast,
            'item': item,
            'fixture': fixture,
            'team': team,
            'team_3': team_3,
            'team_A': team_A,
            'team_B': team_B,
            'team_C': team_C,
            'team_D': team_D,
            'team_E': team_E,
            'team_F': team_F,
            'team_G': team_G,
            'team_H': team_H,
            'teamdb_EN': teamdb_EN,
            'teamdb_ES': teamdb_ES,
            'teamdb_IT': teamdb_IT,
            'teamdb_DE': teamdb_DE,
            'teamdb_FR': teamdb_FR,
            'teamdb_PT': teamdb_PT,
            'teamdb_ND': teamdb_ND,
            'team_rev': team_rev,
            'teamdb': teamdb,
            'form': form,
            'form2': form2
        })
    else:
        print(request.POST)
        print('new forecast')
        try:
            print('try')
            players = Players.objects.get(p_email=request.POST['p_email'])
            i = 0
            v1 = request.POST.getlist('fvalue1')
            v2 = request.POST.getlist('fvalue2')
            v3 = request.POST.getlist('id')
            print(v3)
            xmail = request.POST['p_email']
            for x in v1:
                if v1[i] == '':
                    i = i + 1
                    print(i)

                else:
                    itemi = Items.objects.get(id=v3[i])
                    print(itemi)
                    newforecast=Forecasts.objects.create(f_email=players, fvalue1=v1[i], fvalue2=v2[i], items=itemi)
                    newforecast.ts = timezone.now()
                    try:
                        print('inner try')
                        zzz = Forecasts.objects.get(f_email=xmail, f_isactive=1, items=v3[i])
                        zzz.f_isactive = 0
                        zzz.save()
                    except Exception as error2:
                        print('inner except: ', error2)

                    newforecast.f_isactive = 1
                    if v2[i] == '':
                        newforecast.f1x2 = ''
                    elif v1[i] == v2[i]:
                        newforecast.f1x2 = 'x'
                    elif v1[i] > v2[i]:
                        newforecast.f1x2 = '1'
                    elif v1[i] < v2[i]:
                        newforecast.f1x2 = '2'
                    else:
                        newforecast.f1x2 = ''
                    newforecast.save()
                    i = i + 1
                    print('saved')
                    print(i)

            
            return redirect('forecasts')


        except Exception as error:
            print('except: ', error)
            return render(request, 'forecasts.html', {
                'forecast': forecast,
                'item': item,
                'fixture': fixture,
                'team': team,
                'teamdb': teamdb,
                'form': form,
                'error': 'Player not registered. Try new email.'
            })

    print('Forecasted')
    return render(request, 'forecast.html')

def standings(request):

    print('Standings')   

    data = Items.objects.filter(editions=33, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    print('data', data-38)

    items = Forecasts.objects.filter(items__editions=33, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)

    stnd = items.values('f_email').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        w=F('f_email__winnable'),
        p=F('f_email__paid'),
        stars=F('f_email__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates=data)),
        dlt2=Sum(('points'),filter=Q(items__dates=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
    ).order_by('-tot', '-tot2', '-fn')
    print('stnd', stnd)

    stats = stnd.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
    )
    print('stats', stats)

    if request.method == 'GET':
        return render(request, 'standings.html', {
            'standings': stnd,
            'stats': stats,
        })

def statistics(request):
        
    print('Statistics')
    
    data = Items.objects.filter(editions=33, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    data0 = data - 38
    data1 = data - 39
    data2 = data - 40
    data3 = data - 41
    data4 = data - 42
    print('data', data-38)
    items = Forecasts.objects.filter(items__editions=33, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)
    stnd = items.values('f_email').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        w=F('f_email__winnable'),
        p=F('f_email__paid'),
        stars=F('f_email__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates=data)),
        dlt2=Sum(('points'),filter=Q(items__dates=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
    ).order_by('-tot', '-tot2', '-fn')
    print('stnd', stnd)
    stnd5 = stnd[:5]
    stats = stnd.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
    )
    print('stats', stats)
    
    stnd4 = items.values('f_email').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        stars=F('f_email__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates__lte=data)),
        dlt2=Sum(('points'),filter=Q(items__dates__lte=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates__lte=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates__lte=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates__lte=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
    ).order_by('-tot', '-fn')
    print('stnd4', stnd4)

    stats4 = stnd4.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
        maxdlt2=Max('dlt2'),
        mindlt2=Min('dlt2'),
        avgdlt2=Avg('dlt2'),
        sumdlt2=Sum('dlt2'),
        cntdlt2=Count('dlt2'),
        maxdlt3=Max('dlt3'),
        mindlt3=Min('dlt3'),
        avgdlt3=Avg('dlt3'),
        sumdlt3=Sum('dlt3'),
        cntdlt3=Count('dlt3'),
        maxdlt4=Max('dlt4'),
        mindlt4=Min('dlt4'),
        avgdlt4=Avg('dlt4'),
        sumdlt4=Sum('dlt4'),
        cntdlt4=Count('dlt4'),
        maxdlt5=Max('dlt5'),
        mindlt5=Min('dlt5'),
        avgdlt5=Avg('dlt5'),
        sumdlt5=Sum('dlt5'),
        cntdlt5=Count('dlt5'),
    )
    print('stats4', stats4)

    return render(request, 'statistics.html', {
            'standings': stnd5,
            'stats': stats,
            'data': data-38,
            'data0': data0,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'standings4': stnd4,
            'stats4': stats4,
        })

def footballdata(request):
    uri = 'https://api.football-data.org/v2/competitions/2001/teams/'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }

    response = requests.get(uri, headers=headers)

#    matches = response.json()['matches']
    matches = response.json()['teams']
#    print(json.dumps(matches, indent=4, sort_keys=True))
    print(matches)

    if request.method == 'GET':
        return render(request, 'footballdata.html', {
            'match': matches,
        })
    
def oldforecasts(request):

    players = Players.objects.all()
    formP = PlayersForm

    if request.method == 'GET':
        return render(request, 'oldforecasts.html', {
            'players': players,
            'form': formP,
        })
    else:
        forecasts = Forecasts.objects.filter(f_email=request.POST['mail'], f_isactive=1).order_by('items_id')
        player = Players.objects.get(p_email=request.POST['mail'])
        items = Items.objects.filter(editions=33)
        teams = Teams.objects.all()
        teamsDB = Teamsdb.objects.all()
        scores = Scores.objects.all
        dates = Dates.objects.all
        rounds = Rounds.objects.all
        stages = Stages.objects.all
#        mail = request.POST['mail']
        formF = ForecastsForm
        return render(request, 'oldforecasts.html', {
            'forecasts': forecasts,
            'form': formF,
#            'email': mail,
            'player': player,
            'items': items,
            'teams': teams,
            'teamsDB': teamsDB,
            'scores': scores,
            'dates': dates,
            'rounds': rounds,
            'stages': stages,
        })
    
def pointstable(request):

    items = Items.objects.filter(editions=33,open__lte=timezone.now())
    items_len = Items.objects.filter(editions=33,open__lte=timezone.now()).count()
    forecasts = Forecasts.objects.filter(f_isactive=1, items__editions=33, items__open__lte=timezone.now())
    players = Players.objects.all().order_by('p_email')
    players_len = Players.objects.all().count()
    i=0
    j=0
    valuexy = np.empty((items_len,players_len), dtype=object)

    for x in items:
        for y in players:
            valuexy[i,j] = forecasts.filter(items=x, f_email=y).order_by('items', 'f_email').first()
            j += 1
        i += 1
        j = 0

    print('done')
# review starting here

    if request.method == 'GET':
        return render(request, 'pointstable.html', {
            'players': players,
            'array': valuexy,
        })
    else:
        return render(request, 'pointstable.html', {
            'players': players,
        })

def apiresults(request):
    uri = 'https://api.football-data.org/v2/competitions/2001/matches/'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }

    response = requests.get(uri, headers=headers)

    print(response.json())
    matches = response.json()['matches']
    teams = Teams.objects.all()
    teamsdb = Teamsdb.objects.all()

#    matches = response.json()['teams']
#    print(json.dumps(matches, indent=4, sort_keys=True))
    print(matches)

    if request.method == 'GET':
        return render(request, 'apiresults.html', {
            'match': matches,
            'teams':teams,
            'teamsdb':teamsdb,
        })
    
def communities(request):

    print('Communities')

    data = Items.objects.filter(editions=33, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    print('data', data-38)
    items0 = Forecasts.objects.filter(items__editions=33, f_isactive=1, ts__lte=timezone.now())
    test0 = items0.values('f_email').annotate(
        pts=Sum(('points'),filter=Q(items__dates__lte=data)),
        dlt=Sum(('points'),filter=Q(items__dates=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        w=F('f_email__winnable'),
        p=F('f_email__paid'),
        stars=F('f_email__playerdb_id__stars'),
    ).order_by('-pts', '-stars', 'fn')
 
    if request.method == 'GET':
        return render(request, 'communities.html', {
            'test': test0,
        })

def proves(request):

    print('Proves')

    data = Items.objects.filter(editions=33, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    data0 = data - 38
    data1 = data - 39
    data2 = data - 40
    data3 = data - 41
    data4 = data - 42
    print('data', data-38)
    items = Forecasts.objects.filter(items__editions=33, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)
    stnd = items.values('items__dates', 'f_email').annotate(
        dlt=Sum('points'),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        stars=F('f_email__playerdb_id__stars'),
    ).order_by('-items__dates', '-dlt', 'fn')
    print('stnd', stnd)

    stnd2 = items.values('items__dates').annotate(
        tot=Sum('points'),
        avgdlt=Avg('points'),
    ).order_by('-items__dates', '-tot')
    print('stnd2', stnd2)

    stats = stnd.aggregate(
        maxdlt=Max('dlt'),
        mindlt=Min('dlt'),
        avgdlt=Avg('dlt'),
        sumdlt=Sum('dlt'),
        cntdlt=Count('dlt'),
    )
    print('stats', stats)

    stnd3 = items.values('f_email').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        stars=F('f_email__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates=data)),
        dlt2=Sum(('points'),filter=Q(items__dates=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
    ).order_by('-tot', '-fn')
    print('stnd3', stnd3)

    stats3 = stnd3.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
        maxdlt2=Max('dlt2'),
        mindlt2=Min('dlt2'),
        avgdlt2=Avg('dlt2'),
        sumdlt2=Sum('dlt2'),
        cntdlt2=Count('dlt2'),
        maxdlt3=Max('dlt3'),
        mindlt3=Min('dlt3'),
        avgdlt3=Avg('dlt3'),
        sumdlt3=Sum('dlt3'),
        cntdlt3=Count('dlt3'),
        maxdlt4=Max('dlt4'),
        mindlt4=Min('dlt4'),
        avgdlt4=Avg('dlt4'),
        sumdlt4=Sum('dlt4'),
        cntdlt4=Count('dlt4'),
        maxdlt5=Max('dlt5'),
        mindlt5=Min('dlt5'),
        avgdlt5=Avg('dlt5'),
        sumdlt5=Sum('dlt5'),
        cntdlt5=Count('dlt5'),
    )
    print('stats3', stats3)

    stnd4 = items.values('f_email').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        stars=F('f_email__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates__lte=data)),
        dlt2=Sum(('points'),filter=Q(items__dates__lte=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates__lte=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates__lte=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates__lte=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
    ).order_by('-tot', '-fn')
    print('stnd4', stnd4)

    stats4 = stnd4.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
        maxdlt2=Max('dlt2'),
        mindlt2=Min('dlt2'),
        avgdlt2=Avg('dlt2'),
        sumdlt2=Sum('dlt2'),
        cntdlt2=Count('dlt2'),
        maxdlt3=Max('dlt3'),
        mindlt3=Min('dlt3'),
        avgdlt3=Avg('dlt3'),
        sumdlt3=Sum('dlt3'),
        cntdlt3=Count('dlt3'),
        maxdlt4=Max('dlt4'),
        mindlt4=Min('dlt4'),
        avgdlt4=Avg('dlt4'),
        sumdlt4=Sum('dlt4'),
        cntdlt4=Count('dlt4'),
        maxdlt5=Max('dlt5'),
        mindlt5=Min('dlt5'),
        avgdlt5=Avg('dlt5'),
        sumdlt5=Sum('dlt5'),
        cntdlt5=Count('dlt5'),
    )
    print('stats4', stats4)

    chart4 = stnd4.values('fn', 'ln', 'dlt1', 'dlt2', 'dlt3', 'dlt4', 'dlt5')
    chartx4 = chart4[:1]

    print('chartx4', chartx4)

# proves de points table alternatiu

    itemsx = Items.objects.filter(editions=33,open__lte=timezone.now())
    itemsx_len = Items.objects.filter(editions=33,open__lte=timezone.now()).count()
    forecastsx = Forecasts.objects.filter(f_isactive=1, items__editions=33, items__open__lte=timezone.now()).annotate(
        itm=F('items__id'),
        emk=F('f_email__p_email'),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        day=F('items__dates'),
        v1=F('items__value1'),
        v2=F('items__value2'),
        field=F('items__fields__id'),
        desc=F('items__description'),
        local=F('items__fixtures__localteam__teamsdb__short'),
        away=F('items__fixtures__awayteam__teamsdb__short'),
    )
    playersx = Players.objects.all().order_by('p_email')
    playersx_len = Players.objects.all().count()
    print('forecastsx', forecastsx)

    if request.method == 'GET':
        return render(request, 'proves.html', {
            'standings': stnd,
            'stats': stats,
            'data': data,
            'data0': data0,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'standings3': stnd3,
            'stats3': stats3,
            'standings4': stnd4,
            'stats4': stats4,
            'chart': chartx4,
            'forecastsx': forecastsx,
            'playersx': playersx,
            'itemsx': itemsx
        })