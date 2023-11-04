from django.shortcuts import render, redirect, HttpResponse
from .models import Items, Fixtures, Teams, Teamsdb, Forecasts, Players, Scores, Dates, Rounds, Stages, Communities, Editions, Dates, Playerdb, Peoples
from .tables import ForecastsTable, UserTable, ItemsTable
from .forms import ItemsForm, ForecastsForm, PlayersForm
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.db.models import Sum, Count, TextField, Q, F, Max, Min, Avg, Func, Window, ExpressionWrapper, Value as V, CharField
from django.db.models.functions import Cast, Rank, DenseRank, ExtractYear, Concat, Substr, ConcatPair
from array import *
from django_pivot.pivot import pivot
import numpy as np
import requests
import json
import django_tables2 as tables
import datetime
import pandas as pd


# Create your views here.

def game(request):
        
    print('Game')
    
    data = Items.objects.filter(editions=33, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    data0 = data - 38
    data1 = data - 39
    data2 = data - 40
    data3 = data - 41
    data4 = data - 42
#    print('data', data-38)
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
    ).order_by('-tot', '-tot2', '-stars', 'fn')
#    print('stnd', stnd)
    stnd5 = stnd[:5]
    stats = stnd.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
    )
#    print('stats', stats)

# codi char.jss

    stnd4 = items.values('f_email').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_email__p_fname'),
        ln=F('f_email__p_lname'),
        name=Concat(Substr('f_email__p_fname', 1, 1), F('f_email__p_lname'), output_field=CharField()),
        stars=F('f_email__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates__lte=data)),
        dlt2=Sum(('points'),filter=Q(items__dates__lte=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates__lte=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates__lte=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates__lte=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
    ).order_by('-tot', '-tot2', '-stars', 'fn')
#    print('stnd4', stnd4)

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

    days = [data4, data3, data2, data1, data0]
    nicks = list(stnd4.values_list('name', flat=True))
    delta1 = list(stnd4.values_list('dlt1', flat=True))
    delta2 = list(stnd4.values_list('dlt2', flat=True))
    delta3 = list(stnd4.values_list('dlt3', flat=True))
    delta4 = list(stnd4.values_list('dlt4', flat=True))
    delta5 = list(stnd4.values_list('dlt5', flat=True))
    print('delta1', delta1)

    listdelta = np.array(nicks)
    listdelta = np.append(listdelta, delta1)
    listdelta = np.append(listdelta, delta2)
    listdelta = np.append(listdelta, delta3)
    listdelta = np.append(listdelta, delta4)
    listdelta = np.append(listdelta, delta5)
    listdelta = np.reshape(listdelta, (6, 42))
    listdelta = np.transpose(listdelta)

    return render(request, 'game.html', {
            'standings': stnd5,
            'stats': stats,
            'data': data-38,
            'labels': days,
            'datax0': list(np.flip(listdelta[0])),
            'datax1': list(np.flip(listdelta[1])),
            'datax2': list(np.flip(listdelta[2])),
            'datax3': list(np.flip(listdelta[3])),
            'datax4': list(np.flip(listdelta[4])),
            'datax5': list(np.flip(listdelta[5])),
            'datax6': list(np.flip(listdelta[6])),
            'datax7': list(np.flip(listdelta[7])),
            'datax8': list(np.flip(listdelta[8])),
            'datax9': list(np.flip(listdelta[9])),
            'datax10': list(np.flip(listdelta[10])),
            'datax11': list(np.flip(listdelta[11])),
            'datax12': list(np.flip(listdelta[12])),
            'datax13': list(np.flip(listdelta[13])),
            'datax14': list(np.flip(listdelta[14])),
            'datax15': list(np.flip(listdelta[15])),
            'datax16': list(np.flip(listdelta[16])),
            'datax17': list(np.flip(listdelta[17])),
            'datax18': list(np.flip(listdelta[18])),
            'datax19': list(np.flip(listdelta[19])),
            'datax20': list(np.flip(listdelta[20])),
            'datax21': list(np.flip(listdelta[21])),
            'datax22': list(np.flip(listdelta[22])),
            'datax23': list(np.flip(listdelta[23])),
            'datax24': list(np.flip(listdelta[24])),
            'datax25': list(np.flip(listdelta[25])),
            'datax26': list(np.flip(listdelta[26])),
            'datax27': list(np.flip(listdelta[27])),
            'datax28': list(np.flip(listdelta[28])),
            'datax29': list(np.flip(listdelta[29])),
            'datax30': list(np.flip(listdelta[30])),
            'datax31': list(np.flip(listdelta[31])),
            'datax32': list(np.flip(listdelta[32])),
            'datax33': list(np.flip(listdelta[33])),
            'datax34': list(np.flip(listdelta[34])),
            'datax35': list(np.flip(listdelta[35])),
            'datax36': list(np.flip(listdelta[36])),
            'datax37': list(np.flip(listdelta[37])),
            'datax38': list(np.flip(listdelta[38])),
            'datax39': list(np.flip(listdelta[39])),
            'datax40': list(np.flip(listdelta[40])),
            'datax41': list(np.flip(listdelta[41])),
            'label0': listdelta[0][0],
            'label1': listdelta[1][0],
            'label2': listdelta[2][0],
            'label3': listdelta[3][0],
            'label4': listdelta[4][0],
            'label5': listdelta[5][0],
            'label6': listdelta[6][0],
            'label7': listdelta[7][0],
            'label8': listdelta[8][0],
            'label9': listdelta[9][0],
            'label10': listdelta[10][0],
            'label11': listdelta[11][0],
            'label12': listdelta[12][0],
            'label13': listdelta[13][0],
            'label14': listdelta[14][0],
            'label15': listdelta[15][0],
            'label16': listdelta[16][0],
            'label17': listdelta[17][0],
            'label18': listdelta[18][0],
            'label19': listdelta[19][0],
            'label20': listdelta[20][0],
            'label21': listdelta[21][0],
            'label22': listdelta[22][0],
            'label23': listdelta[23][0],
            'label24': listdelta[24][0],
            'label25': listdelta[25][0],
            'label26': listdelta[26][0],
            'label27': listdelta[27][0],
            'label28': listdelta[28][0],
            'label29': listdelta[29][0],
            'label30': listdelta[30][0],
            'label31': listdelta[31][0],
            'label32': listdelta[32][0],
            'label33': listdelta[33][0],
            'label34': listdelta[34][0],
            'label35': listdelta[35][0],
            'label36': listdelta[36][0],
            'label37': listdelta[37][0],
            'label38': listdelta[38][0],
            'label39': listdelta[39][0],
            'label40': listdelta[40][0],
            'label41': listdelta[41][0],
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
    ).order_by('-tot', '-tot2', '-stars', 'fn')
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
    ).order_by('-tot', '-tot2', '-stars', 'fn')
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
    ).order_by('-tot', '-tot2', '-stars', 'fn')
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

#   old code points table

#    items = Items.objects.filter(editions=33,open__lte=timezone.now())
#    items_len = Items.objects.filter(editions=33,open__lte=timezone.now()).count()
#    forecasts = Forecasts.objects.filter(f_isactive=1, items__editions=33, items__open__lte=timezone.now())
#    players = Players.objects.all().order_by('p_email')
#    players_len = Players.objects.all().count()
#    i=0
#    j=0
#    valuexy = np.empty((items_len,players_len), dtype=object)

#    for x in items:
#        for y in players:
#            valuexy[i,j] = forecasts.filter(items=x, f_email=y).order_by('items', 'f_email').first()
#            j += 1
#        i += 1
#        j = 0
#    print('done')

# review starting here

    forecasts = Forecasts.objects.filter(f_isactive=1, items__editions=33, items__open__lte=timezone.now()).values('items', 'f_email', 'fvalue1', 'fvalue2').annotate(
        itm=Concat('items__id', V('  '), Substr('items__description', 1, 5), V(' '), Substr('items__fixtures__localteam__teamsdb__short', 1, 3), Substr('items__fixtures__awayteam__teamsdb__short', 1, 3), output_field=CharField()),
        name=Concat(Substr('f_email__p_fname', 1, 1), Substr('f_email__p_lname', 1, 8), output_field=CharField()),
        day=F('items__dates'),
        result=Concat('items__value1','items__value2', output_field=TextField()),
        forec=Concat(Substr('fvalue1', 1, 6), V('..'),'fvalue2', output_field=TextField()),
        field=F('items__fields__id'),
    ).order_by('items', 'f_email')
    forecasts_df = pd.DataFrame(forecasts)
    forecasts_pt = forecasts_df.pivot_table(index='itm', columns='name', values='forec', aggfunc='first')
    forecasts_html = forecasts_pt.to_html(header=True, border=1, table_id='pointstable')
#    print('forecasts_df', forecasts_df)

    if request.method == 'GET':
        return render(request, 'pointstable.html', {
#            'players': players,
#            'array': valuexy,
            'forecasts_html': forecasts_html,
        })
    else:
        return render(request, 'pointstable.html', {
#            'players': players,
            'forecasts_html': forecasts_html,
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
    communities = Communities.objects.all().order_by('name')
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
    ).order_by('-tot', '-tot2', '-stars', 'fn')

    stats = stnd.aggregate(
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
    )

    if request.method == 'GET':
        return render(request, 'communities.html', {
            'standings': stnd,
            'stats': stats,
            'communities': communities,
        })
    else:
        print('POST:', request.POST)
        ctylist = request.POST.getlist('name')
        cty = ctylist[0]
        print('community: ', cty)
        peoples = list(Peoples.objects.filter(communities=cty).values_list('playerdb', flat=True))
        print('peoples: ', peoples)
        items = Forecasts.objects.filter(items__editions=33, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data, f_email__playerdb__in=peoples)
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
        ).order_by('-tot', '-tot2', '-stars', 'fn')
        name = getattr(Communities.objects.get(id=cty),'name')
        print('name: ', name)


        stats = stnd.aggregate(
            maxdlt1=Max('dlt1'),
            mindlt1=Min('dlt1'),
            avgdlt1=Avg('dlt1'),
            sumdlt1=Sum('dlt1'),
            cntdlt1=Count('dlt1'),
        )

        return render(request, 'communities.html', {
            'standings': stnd,
            'stats': stats,
            'communities': communities,
            'name': name,
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
        name=Concat(Substr('f_email__p_fname', 1, 1), F('f_email__p_lname'), output_field=CharField()),
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

    forecasts = Forecasts.objects.filter(f_isactive=1, items__editions=33, items__open__lte=timezone.now()).values('items', 'f_email', 'fvalue1', 'fvalue2').annotate(
        itm=Concat('items__id', V('  '), Substr('items__description', 1, 5), V(' '), Substr('items__fixtures__localteam__teamsdb__short', 1, 3), Substr('items__fixtures__awayteam__teamsdb__short', 1, 3), output_field=CharField()),
        name=Concat(Substr('f_email__p_fname', 1, 1), Substr('f_email__p_lname', 1, 8), output_field=CharField()),
        day=F('items__dates'),
        result=Concat('items__value1','items__value2', output_field=TextField()),
        forec=Concat(Substr('fvalue1', 1, 6), V('..'),'fvalue2', output_field=TextField()),
        field=F('items__fields__id'),
    ).order_by('items', 'f_email')
    forecasts_df = pd.DataFrame(forecasts)
    
    forecasts_pt = forecasts_df.pivot_table(index='itm', columns='name', values='forec', aggfunc='first')
    forecasts_html = forecasts_pt.to_html(header=True, border=1, table_id='pointstable')
#    print('forecasts_html', forecasts_html)

# proves de detecció manca resuultats

    forecastsx2 = Forecasts.objects.filter(f_isactive=1, items__editions=33, items__open__lte=timezone.now()).values_list('items__dates').annotate(
        name=Concat(Substr('f_email__p_fname', 1, 1), Substr('f_email__p_lname', 1, 2), output_field=CharField()),
        emk=F('f_email'),
        cnt=Count('pk')
        ).order_by('f_email', 'items__dates')
    print('forecastsx2', forecastsx2)
    emails = Forecasts.objects.filter(f_isactive=1, items__editions=33, items__open__lte=timezone.now()).values('f_email').distinct().order_by('f_email')
    print('emails', emails)


    pivot2_old = pivot(Forecasts, 'items__dates', 'f_email', 'pk', aggregation=Count)
    pivot2 = list(pivot(forecastsx2, 'items__dates', 'name', 'pk', aggregation=Count))
    print('pivot2', pivot2)

# proves de char.jss

    days = [data4, data3, data2, data1, data0]
    nicks = list(stnd4.values_list('name', flat=True))
    delta1 = list(stnd4.values_list('dlt1', flat=True))
    delta2 = list(stnd4.values_list('dlt2', flat=True))
    delta3 = list(stnd4.values_list('dlt3', flat=True))
    delta4 = list(stnd4.values_list('dlt4', flat=True))
    delta5 = list(stnd4.values_list('dlt5', flat=True))
    print('delta1', delta1)

    listdelta = np.array(nicks)
    listdelta = np.append(listdelta, delta1)
    listdelta = np.append(listdelta, delta2)
    listdelta = np.append(listdelta, delta3)
    listdelta = np.append(listdelta, delta4)
    listdelta = np.append(listdelta, delta5)
    listdelta = np.reshape(listdelta, (6, 42))
    listdelta = np.transpose(listdelta)

#    print('listdelta', (listdelta[2][0]))

# fi proves

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
            'forecasts': forecasts,
            'forecastsx2': forecastsx2,
            'emails': emails,
            'pivot2': pivot2,
            'labels': days,
            'datax0': list(np.flip(listdelta[0])),
            'datax1': list(np.flip(listdelta[1])),
            'datax2': list(np.flip(listdelta[2])),
            'datax3': list(np.flip(listdelta[3])),
            'datax4': list(np.flip(listdelta[4])),
            'datax5': list(np.flip(listdelta[5])),
            'datax6': list(np.flip(listdelta[6])),
            'datax7': list(np.flip(listdelta[7])),
            'datax8': list(np.flip(listdelta[8])),
            'datax9': list(np.flip(listdelta[9])),
            'datax10': list(np.flip(listdelta[10])),
            'datax11': list(np.flip(listdelta[11])),
            'datax12': list(np.flip(listdelta[12])),
            'datax13': list(np.flip(listdelta[13])),
            'datax14': list(np.flip(listdelta[14])),
            'datax15': list(np.flip(listdelta[15])),
            'datax16': list(np.flip(listdelta[16])),
            'datax17': list(np.flip(listdelta[17])),
            'datax18': list(np.flip(listdelta[18])),
            'datax19': list(np.flip(listdelta[19])),
            'datax20': list(np.flip(listdelta[20])),
            'datax21': list(np.flip(listdelta[21])),
            'datax22': list(np.flip(listdelta[22])),
            'datax23': list(np.flip(listdelta[23])),
            'datax24': list(np.flip(listdelta[24])),
            'datax25': list(np.flip(listdelta[25])),
            'datax26': list(np.flip(listdelta[26])),
            'datax27': list(np.flip(listdelta[27])),
            'datax28': list(np.flip(listdelta[28])),
            'datax29': list(np.flip(listdelta[29])),
            'datax30': list(np.flip(listdelta[30])),
            'datax31': list(np.flip(listdelta[31])),
            'datax32': list(np.flip(listdelta[32])),
            'datax33': list(np.flip(listdelta[33])),
            'datax34': list(np.flip(listdelta[34])),
            'datax35': list(np.flip(listdelta[35])),
            'datax36': list(np.flip(listdelta[36])),
            'datax37': list(np.flip(listdelta[37])),
            'datax38': list(np.flip(listdelta[38])),
            'datax39': list(np.flip(listdelta[39])),
            'datax40': list(np.flip(listdelta[40])),
            'datax41': list(np.flip(listdelta[41])),
            'label0': listdelta[0][0],
            'label1': listdelta[1][0],
            'label2': listdelta[2][0],
            'label3': listdelta[3][0],
            'label4': listdelta[4][0],
            'label5': listdelta[5][0],
            'label6': listdelta[6][0],
            'label7': listdelta[7][0],
            'label8': listdelta[8][0],
            'label9': listdelta[9][0],
            'label10': listdelta[10][0],
            'label11': listdelta[11][0],
            'label12': listdelta[12][0],
            'label13': listdelta[13][0],
            'label14': listdelta[14][0],
            'label15': listdelta[15][0],
            'label16': listdelta[16][0],
            'label17': listdelta[17][0],
            'label18': listdelta[18][0],
            'label19': listdelta[19][0],
            'label20': listdelta[20][0],
            'label21': listdelta[21][0],
            'label22': listdelta[22][0],
            'label23': listdelta[23][0],
            'label24': listdelta[24][0],
            'label25': listdelta[25][0],
            'label26': listdelta[26][0],
            'label27': listdelta[27][0],
            'label28': listdelta[28][0],
            'label29': listdelta[29][0],
            'label30': listdelta[30][0],
            'label31': listdelta[31][0],
            'label32': listdelta[32][0],
            'label33': listdelta[33][0],
            'label34': listdelta[34][0],
            'label35': listdelta[35][0],
            'label36': listdelta[36][0],
            'label37': listdelta[37][0],
            'label38': listdelta[38][0],
            'label39': listdelta[39][0],
            'label40': listdelta[40][0],
            'label41': listdelta[41][0],
        })
    
def proves2(request):
        
    print('Proves2')

    labels = []
    datax = []
    dataxx = []
    dataxxx = []


    queryset = Playerdb.objects.all()[:5]
    print(queryset)
    for player in queryset:
        labels.append(player.lname)
        datax.append(player.pk)
        dataxx.append(player.pk * 3)
        dataxxx.append(player.pk + 5)
    print ('datax', datax)
    print ('dataxx', dataxx)
    print ('dataxxx', dataxxx)
    print ('labels', labels)
    
    return render(request, 'proves2.html', {
        'data': datax,
        'data2': dataxx,
        'data3': dataxxx,
        'labels': labels,
        })