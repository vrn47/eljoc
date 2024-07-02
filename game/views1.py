from django.shortcuts import render, redirect, HttpResponse
from .models import Items, Fixtures, Teams, Teamsdb, Forecasts, Players, Scores, Dates, Rounds, Stages, Communities, Editions, Dates, Playerdb, Peoples
from .tables import ForecastsTable, UserTable, ItemsTable
from .forms import ItemsForm, ForecastsForm, PlayersForm
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.db.models import Sum, Count, TextField, Q, F, Max, Min, Avg, Func, Window, ExpressionWrapper, Value as V, CharField, Value
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
    
    currentedition = 34
#   suprimir el "+1" quan arrenqui la competició.
    data = Items.objects.filter(editions=currentedition, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    print('data', data)
    data0 = data - 83
    data1 = data - 84
    data2 = data - 85
    data3 = data - 86
    data4 = data - 87
    print('data0', data0)
    if data0 == 0:
            return render(request, 'game.html', {
            'data': data-83,
            })

    else:
        items = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)
        print('items', items)
        stnd = items.values('f_player').annotate(
            tot=Sum('points'),
            tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
            fn=F('f_player__p_fname'),
            ln=F('f_player__p_lname'),
            w=F('f_player__winnable'),
            p=F('f_player__paid'),
            stars=F('f_player__playerdb_id__stars'),
            dlt1=Sum(('points'),filter=Q(items__dates=data)),
            dlt2=Sum(('points'),filter=Q(items__dates=data-1)),
            dlt3=Sum(('points'),filter=Q(items__dates=data-2)),
            dlt4=Sum(('points'),filter=Q(items__dates=data-3)),
            dlt5=Sum(('points'),filter=Q(items__dates=data-4)),
            rank0=Window(expression=Rank(),order_by=F('tot').desc()),
            rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
            top=Sum(('items__scores__s_max'),filter=Q(items__dates=data)),
        ).order_by('-tot', '-tot2', '-stars', 'fn')
        print('stnd', stnd)
        stnd5 = stnd[:5]
        stats = stnd.aggregate(
            maxdlt1=Max('dlt1'),
            mindlt1=Min('dlt1'),
            avgdlt1=Avg('dlt1'),
            sumdlt1=Sum('dlt1'),
            cntdlt1=Count('dlt1'),
            topdlt1=Avg('top'),
        )
    #    print('stats', stats)

    # codi char.jss

        stnd4 = items.values('f_player').annotate(
            tot=Sum('points'),
            tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
            fn=F('f_player__p_fname'),
            ln=F('f_player__p_lname'),
            name=Concat(Substr('f_player__p_fname', 1, 1), F('f_player__p_lname'), output_field=CharField()),
            stars=F('f_player__playerdb_id__stars'),
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
        mida = listdelta.size
        print('mida', mida)
        listdelta = np.append(listdelta, delta1)
        listdelta = np.append(listdelta, delta2)
        listdelta = np.append(listdelta, delta3)
        listdelta = np.append(listdelta, delta4)
        listdelta = np.append(listdelta, delta5)
    # compte que el 44 d'aquí sota és el nombre de jugadors actius
        listdelta = np.reshape(listdelta, (6, mida))
        listdelta = np.transpose(listdelta)
        print('listdelta', listdelta)
        print('datax0', list(np.flip(listdelta[41])))
        print('label0', listdelta[41][0])

        return render(request, 'game.html', {
                'standings': stnd5,
                'stats': stats,
                'data': data0,
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
    currentedition = 34
    time = timezone.now()
    print(time)    
    item = Items.objects.filter(open__lt=time,close__gt=time, ).exclude(fields_id=1).exclude(fields_id=6)
    fixture = Fixtures.objects.all()
    team = Teams.objects.filter(editions=currentedition).order_by('coef')
    team_3 = Teams.objects.filter(editions=currentedition).order_by('-coef')
    team_A = Teams.objects.filter(editions=currentedition, grp='A').order_by('pos')
    team_B = Teams.objects.filter(editions=currentedition, grp='B').order_by('pos')
    team_C = Teams.objects.filter(editions=currentedition, grp='C').order_by('pos')
    team_D = Teams.objects.filter(editions=currentedition, grp='D').order_by('pos')
    team_E = Teams.objects.filter(editions=currentedition, grp='E').order_by('pos')
    team_F = Teams.objects.filter(editions=currentedition, grp='F').order_by('pos')
    team_G = Teams.objects.filter(editions=currentedition, grp='G').order_by('pos')
    team_H = Teams.objects.filter(editions=currentedition, grp='H').order_by('pos')
    team_rev = Teams.objects.filter(editions=currentedition, rev=1).order_by('-coef')
    teamdb = Teamsdb.objects.all()
    teamdb_WC = Teamsdb.objects.filter(world_id=1, is_club=1)
    teamdb_EN = Teamsdb.objects.filter(fed='ENG').order_by('id')
    teamdb_ES = Teamsdb.objects.filter(fed='ESP').order_by('id')
    teamdb_IT = Teamsdb.objects.filter(fed='ITA').order_by('id')
    teamdb_DE = Teamsdb.objects.filter(fed='DEU').order_by('id')
    teamdb_FR = Teamsdb.objects.filter(fed='FRA').order_by('id')
    teamdb_PT = Teamsdb.objects.filter(fed='POR').order_by('id')
    teamdb_ND = Teamsdb.objects.filter(fed='NED').order_by('id')
    teamdb_1st = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=1).order_by('teams__grp')
    teamdb_1stA = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='A')
    teamdb_1stB = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='B')
    teamdb_1stC = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='C')
    teamdb_1stD = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='D')
    teamdb_1stE = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='E')
    teamdb_1stF = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='F')
#    teamdb_1stG = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='G')
#    teamdb_1stH = Teamsdb.objects.get(teams__editions=currentedition,teams__pos=1,teams__grp='H')
    teamdb_2nd = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp')
    teamdb_2ndA = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='A').exclude(fed=teamdb_1stA.fed)
    teamdb_2ndB = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='B').exclude(fed=teamdb_1stB.fed)
    teamdb_2ndC = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='C').exclude(fed=teamdb_1stC.fed)
    teamdb_2ndD = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='D').exclude(fed=teamdb_1stD.fed)
    teamdb_2ndE = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='E').exclude(fed=teamdb_1stE.fed)
    teamdb_2ndF = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='F').exclude(fed=teamdb_1stF.fed)
#    teamdb_2ndG = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='G').exclude(fed=teamdb_1stG.fed)
#    teamdb_2ndH = Teamsdb.objects.filter(teams__editions=currentedition,teams__pos=2).order_by('teams__grp').exclude(teams__grp='H').exclude(fed=teamdb_1stH.fed)
    teamRo16_1 = Teamsdb.objects.filter(teams__id=84) | Teamsdb.objects.filter(teams__id=77).order_by('teams__pos')
    teamRo16_2 = Teamsdb.objects.filter(teams__id=75) | Teamsdb.objects.filter(teams__id=70).order_by('teams__pos')
    teamRo16_3 = Teamsdb.objects.filter(teams__id=71) | Teamsdb.objects.filter(teams__id=85).order_by('teams__pos')
    teamRo16_4 = Teamsdb.objects.filter(teams__id=72) | Teamsdb.objects.filter(teams__id=74).order_by('teams__pos')
    teamRo16_5 = Teamsdb.objects.filter(teams__id=73) | Teamsdb.objects.filter(teams__id=67).order_by('teams__pos')
    teamRo16_6 = Teamsdb.objects.filter(teams__id=80) | Teamsdb.objects.filter(teams__id=86).order_by('teams__pos')
    teamRo16_7 = Teamsdb.objects.filter(teams__id=81) | Teamsdb.objects.filter(teams__id=78).order_by('teams__pos')
    teamRo16_8 = Teamsdb.objects.filter(teams__id=66) | Teamsdb.objects.filter(teams__id=87).order_by('teams__pos')
    teamQF = Teamsdb.objects.filter(teams__editions=33,teams__round__id=4).order_by('id')
    teamQF_1 = Teamsdb.objects.filter(teams__id=72) | Teamsdb.objects.filter(teams__id=75).order_by('teams__pos')
    teamQF_2 = Teamsdb.objects.filter(teams__id=80) | Teamsdb.objects.filter(teams__id=73).order_by('teams__pos')
    teamQF_3 = Teamsdb.objects.filter(teams__id=71) | Teamsdb.objects.filter(teams__id=84).order_by('teams__pos')
    teamQF_4 = Teamsdb.objects.filter(teams__id=78) | Teamsdb.objects.filter(teams__id=87).order_by('teams__pos')
    teamSF_1 = Teamsdb.objects.filter(teams__id=35) | Teamsdb.objects.filter(teams__id=37).order_by('teams__pos')
    teamSF_2 = Teamsdb.objects.filter(teams__id=55) | Teamsdb.objects.filter(teams__id=53).order_by('teams__pos')
    teamW = Teamsdb.objects.filter(teams__id=37) | Teamsdb.objects.filter(teams__id=55).order_by('teams__pos')
    # print('TeamQF: ', teamQF)

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
            'teamdb_WC': teamdb_WC,
            'teamdb_EN': teamdb_EN,
            'teamdb_ES': teamdb_ES,
            'teamdb_IT': teamdb_IT,
            'teamdb_DE': teamdb_DE,
            'teamdb_FR': teamdb_FR,
            'teamdb_PT': teamdb_PT,
            'teamdb_ND': teamdb_ND,
            'teamdb_1st': teamdb_1st,
            'teamdb_1stA': teamdb_1stA,
            'teamdb_1stB': teamdb_1stB,
            'teamdb_1stC': teamdb_1stC,
            'teamdb_1stD': teamdb_1stD,
            'teamdb_1stE': teamdb_1stE,
            'teamdb_1stF': teamdb_1stF,
#            'teamdb_1stG': teamdb_1stG,
#            'teamdb_1stH': teamdb_1stH,
            'teamdb_2nd': teamdb_2nd,
            'teamdb_2ndA': teamdb_2ndA,
            'teamdb_2ndB': teamdb_2ndB,
            'teamdb_2ndC': teamdb_2ndC,
            'teamdb_2ndD': teamdb_2ndD,
            'teamdb_2ndE': teamdb_2ndE,
            'teamdb_2ndF': teamdb_2ndF,
#            'teamdb_2ndG': teamdb_2ndG,
#            'teamdb_2ndH': teamdb_2ndH,
            'teamRo16_1': teamRo16_1,
            'teamRo16_2': teamRo16_2,
            'teamRo16_3': teamRo16_3,
            'teamRo16_4': teamRo16_4,
            'teamRo16_5': teamRo16_5,
            'teamRo16_6': teamRo16_6,
            'teamRo16_7': teamRo16_7,
            'teamRo16_8': teamRo16_8,
            'teamQF': teamQF,
            'teamQF_1': teamQF_1,
            'teamQF_2': teamQF_2,
            'teamQF_3': teamQF_3,
            'teamQF_4': teamQF_4,
            'teamSF_1': teamSF_1,
            'teamSF_2': teamSF_2,
            'teamW': teamW,
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
            playersedition = Players.objects.filter(editions=currentedition)
            print('playersedition', playersedition)
            playeredition = playersedition.get(p_email=request.POST['p_email'])
            print('playeredition', playeredition)
            playerid = getattr(playeredition, 'id')
            edition = getattr(getattr(playeredition, 'editions'), 'id')
#            players = Players.objects.get(p_email=request.POST['p_email'])
            i = 0
            v1 = request.POST.getlist('fvalue1')
            v2 = request.POST.getlist('fvalue2')
            v3 = request.POST.getlist('id')
#            print(v3, v2, v1)
            xmail = request.POST['p_email']
            for x in v1:
                if v1[i] == '':
                    i = i + 1
                    print('buit', i)

                else:
                    itemi = Items.objects.get(id=v3[i])
#                    print(itemi)
                    newforecast=Forecasts.objects.create(f_email=xmail, fvalue1=v1[i], fvalue2=v2[i], items=itemi, f_player=playeredition)
#                    print(newforecast)
                    newforecast.ts = timezone.now()
                    try:
                        print('inner try')
                        zzz = Forecasts.objects.get(f_email=xmail, f_isactive=1, items=v3[i])
#                        print(zzz)
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
                    print('ple', i)

            
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

    currentedition = 34
#   suprimir el "+1" quan arrenqui la competició.
    data = Items.objects.filter(editions=currentedition, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    data0 = data - 83
    print('data', data, 'data0', data0)

    items = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)
    print('items', items)

    stnd = items.values('f_player').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        w=F('f_player__winnable'),
        p=F('f_player__paid'),
        stars=F('f_player__playerdb_id__stars'),
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
    
    currentedition = 34
#   suprimir el "+1" quan arrenqui la competició.
    data = Items.objects.filter(editions=currentedition, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    data0 = data - 83
    data1 = data - 84
    data2 = data - 85
    data3 = data - 86
    data4 = data - 87
    print('data', data-83)
    dates0 = Dates.objects.get(id=data)
    dates1 = Dates.objects.get(id=data-1)
    dates2 = Dates.objects.get(id=data-2)
    dates3 = Dates.objects.get(id=data-3)
    dates4 = Dates.objects.get(id=data-4)
    items = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)
    stnd = items.values('f_player').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        w=F('f_player__winnable'),
        p=F('f_player__paid'),
        stars=F('f_player__playerdb_id__stars'),
        dlt1=Sum(('points'),filter=Q(items__dates=data)),
        dlt2=Sum(('points'),filter=Q(items__dates=data-1)),
        dlt3=Sum(('points'),filter=Q(items__dates=data-2)),
        dlt4=Sum(('points'),filter=Q(items__dates=data-3)),
        dlt5=Sum(('points'),filter=Q(items__dates=data-4)),
        rank0=Window(expression=Rank(),order_by=F('tot').desc()),
        rank1=Window(expression=Rank(),order_by=F('tot2').desc()),
        top=Sum(('items__scores__s_max'),filter=Q(items__dates=data)),
    ).order_by('-tot', '-tot2', '-stars', 'fn')
    print('stnd', stnd)
    stnd5 = stnd[:5]
    stats = stnd.aggregate(
        topdlt1=Avg('top'),
        maxdlt1=Max('dlt1'),
        mindlt1=Min('dlt1'),
        avgdlt1=Avg('dlt1'),
        sumdlt1=Sum('dlt1'),
        cntdlt1=Count('dlt1'),
    )
    print('stats', stats)
    
    stnd4 = items.values('f_player').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        stars=F('f_player__playerdb_id__stars'),
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

#    teams stats

    teams = Teams.objects.filter(editions=currentedition)
    best = teams.values('id').annotate(
        Pts=Sum(F('ptsgs') + F('ptsko')),
        Name=F('teamsdb__name'),
        Short=F('teamsdb__short'),
    ).order_by('-Pts')[:3]
    print('best', best)
    revGS = teams.values('id').annotate(
        Pts=Sum(F('ptsgs') * F('coef') * F('rev')),
        Coef=F('coef'),
        Name=F('teamsdb__name'),
        Short=F('teamsdb__short'),
    ).order_by('-Pts')[:3]
    print('revGS', revGS)
    rev = teams.values('id').annotate(
        Pts=Sum((F('ptsgs') + F('ptsko')) * F('coef') * F('rev')),
        Coef=F('coef'),
        Name=F('teamsdb__name'),
        Short=F('teamsdb__short'),
    ).order_by('-Pts')[:3]
    print('rev', rev)
    worst = teams.values('id').annotate(
        Pts=Sum(F('ptsgs')),
        Name=F('teamsdb__name'),
        Short=F('teamsdb__short'),
    ).order_by('Pts')[:3]
    print('worst', worst)
    crash = teams.values('id').annotate(
        Round=F('round'),
        Coef=F('coef'),
        Name=F('teamsdb__name'),
        Short=F('teamsdb__short'),
    ).order_by('Round', 'Coef')[:3]
    print('crash', crash)

#    player stats

    uri = 'https://api.football-data.org/v4/competitions/2018//scorers/'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }
    response_scorers = requests.get(uri, headers=headers)
#    print('rsp scorers', response_scorers.json())
    scorers = response_scorers.json()['scorers']
#    print('scorers', scorers[:10])


    return render(request, 'statistics.html', {
            'standings': stnd5,
            'stats': stats,
            'dates0': dates0,
            'dates1': dates1,
            'dates2': dates2,
            'dates3': dates3,
            'dates4': dates4,
            'data': data,
            'data0': data0,
            'data1': data1,
            'data2': data2,
            'data3': data3,
            'data4': data4,
            'standings4': stnd4,
            'stats4': stats4,
            'best': best,
            'crash': crash,
            'worst': worst,
            'rev': rev,
            'revGS': revGS,
            'scorers': scorers,
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

    currentedition = 34
    players = Players.objects.all()
    formP = PlayersForm

    if request.method == 'GET':
        return render(request, 'oldforecasts.html', {
            'players': players,
            'form': formP,
        })
    else:
        forecasts = Forecasts.objects.filter(items__editions=currentedition, f_email=request.POST['mail'], f_isactive=1, ).order_by('items_id')
        player = Players.objects.get(editions=currentedition, p_email=request.POST['mail'])
        items = Items.objects.filter(editions=currentedition)
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

    currentedition = 34
    forecasts = Forecasts.objects.filter(f_isactive=1, items__editions=currentedition, items__open__lte=timezone.now()).values('items', 'f_player', 'f_email', 'fvalue1', 'fvalue2').annotate(
        itm=Concat('items__id', V('  '), Substr('items__description', 1, 5), V(' '), Substr('items__fixtures__localteam__teamsdb__short', 1, 3), Substr('items__fixtures__awayteam__teamsdb__short', 1, 3), output_field=CharField()),
        name=Concat(Substr('f_player__p_fname', 1, 1), Substr('f_player__p_lname', 1, 8), output_field=CharField()),
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
    uri = 'https://api.football-data.org/v4/competitions/2001/matches/'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }

    response = requests.get(uri, headers=headers)

    print(response.json())
    matches = response.json()['matches']
    teams = Teams.objects.all()
    teamsdb = Teamsdb.objects.all()
    fixtures = Fixtures.objects.all()

#    matches = response.json()['teams']
#    print(json.dumps(matches, indent=4, sort_keys=True))
    print(matches)

    if request.method == 'GET':
        return render(request, 'apiresults.html', {
            'match': matches,
            'teams':teams,
            'teamsdb':teamsdb,
            'fictures': fixtures,
        })
    
def communities(request):

    print('Communities')

    currentedition = 34
    data = Items.objects.filter(editions=currentedition, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    print('data', data-38)
    communities = Communities.objects.all().order_by('name')
    items = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)
    stnd = items.values('f_player').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        w=F('f_player__winnable'),
        p=F('f_player__paid'),
        stars=F('f_player__playerdb_id__stars'),
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
        items = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data, f_player__playerdb__in=peoples)
        stnd = items.values('f_player').annotate(
            tot=Sum('points'),
            tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
            fn=F('f_player__p_fname'),
            ln=F('f_player__p_lname'),
            w=F('f_player__winnable'),
            p=F('f_player__paid'),
            stars=F('f_player__playerdb_id__stars'),
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

    currentedition = 34
    data = Items.objects.filter(editions=currentedition, value1__isnull=False).order_by('-dates').values_list('dates', flat=True).first()
    data0 = data - 83
    data1 = data - 84
    data2 = data - 85
    data3 = data - 86
    data4 = data - 87
    print('data', data-83)
    items = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, ts__lte=timezone.now(),items__dates__lte=data)
    stnd = items.values('items__dates', 'f_player').annotate(
        dlt=Sum('points'),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        stars=F('f_player__playerdb_id__stars'),
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

    stnd3 = items.values('f_player').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        stars=F('f_player__playerdb_id__stars'),
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

    stnd4 = items.values('f_player').annotate(
        tot=Sum('points'),
        tot2=Sum(('points'),filter=Q(items__dates__lt=data)),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        name=Concat(Substr('f_player__p_fname', 1, 1), F('f_player__p_lname'), output_field=CharField()),
        stars=F('f_player__playerdb_id__stars'),
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

# Proves de bonus
    
    itemsB = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, items__dates__round=2).exclude(items__dates=98)
    print('itemsB', itemsB)
    stndB = itemsB.values('f_player').annotate(
        Tot=Sum('points'),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        em=F('f_player__p_email'),
        id=F('f_player__id'),
        stars=F('f_player__playerdb_id__stars'),
        Rank=Window(expression=Rank(),order_by=F('Tot').desc()),
        bon=Value(26),
        Pts=F('Rank')
    ).order_by('-Tot', 'fn')
    print('stndB', stndB)

    itemsC = Forecasts.objects.filter(items__editions=currentedition, f_isactive=1, items__dates__round__stage=3).exclude(items__dates=114)
    print('itemsC', itemsC)
    stndC = itemsC.values('f_player').annotate(
        Tot=Sum('points'),
        fn=F('f_player__p_fname'),
        ln=F('f_player__p_lname'),
        em=F('f_player__p_email'),
        id=F('f_player__id'),
        stars=F('f_player__playerdb_id__stars'),
        Rank=Window(expression=Rank(),order_by=F('Tot').desc()),
        bon=Value(26),
        Pts=F('Rank')
    ).order_by('-Tot', 'fn')
    print('stndC', stndC)



# proves de points table alternatiu

    forecasts = Forecasts.objects.filter(f_isactive=1, items__editions=currentedition, items__open__lte=timezone.now()).values('items', 'f_player', 'f_email', 'fvalue1', 'fvalue2').annotate(
        itm=Concat('items__id', V('  '), Substr('items__description', 1, 5), V(' '), Substr('items__fixtures__localteam__teamsdb__short', 1, 3), Substr('items__fixtures__awayteam__teamsdb__short', 1, 3), output_field=CharField()),
        name=Concat(Substr('f_player__p_fname', 1, 1), Substr('f_player__p_lname', 1, 8), output_field=CharField()),
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

    forecastsx2 = Forecasts.objects.filter(f_isactive=1, items__editions=currentedition, items__open__lte=timezone.now()).values_list('items__dates').annotate(
        name=Concat(Substr('f_player__p_fname', 1, 1), Substr('f_player__p_lname', 1, 2), output_field=CharField()),
        emk=F('f_email'),
        cnt=Count('pk')
        ).order_by('f_email', 'items__dates')
    print('forecastsx2', forecastsx2)
    emails = Forecasts.objects.filter(f_isactive=1, items__editions=currentedition, items__open__lte=timezone.now()).values('f_email').distinct().order_by('f_email')
    print('emails', emails)


    pivot2_old = pivot(Forecasts, 'items__dates', 'f_email', 'pk', aggregation=Count)
    pivot2 = list(pivot(forecastsx2, 'items__dates', 'name', 'pk', aggregation=Count))
    print('pivot2', pivot2)

# proves de char.js
    
    if data0 == 0:
        print('no info for chart')
        days = [data4, data3, data2, data1, data0]
        listdelta = [0, 0]

    else:
        days = [data4, data3, data2, data1, data0]
        nicks = list(stnd4.values_list('name', flat=True))
        delta1 = list(stnd4.values_list('dlt1', flat=True))
        delta2 = list(stnd4.values_list('dlt2', flat=True))
        delta3 = list(stnd4.values_list('dlt3', flat=True))
        delta4 = list(stnd4.values_list('dlt4', flat=True))
        delta5 = list(stnd4.values_list('dlt5', flat=True))
        print('delta1', delta1)
        print('delta2', delta2)

        listdelta = np.array(nicks)
        mida = listdelta.size
        listdelta = np.append(listdelta, delta1)
        listdelta = np.append(listdelta, delta2)
        listdelta = np.append(listdelta, delta3)
        listdelta = np.append(listdelta, delta4)
        listdelta = np.append(listdelta, delta5)
        listdelta = np.reshape(listdelta, (6, mida))
        listdelta = np.transpose(listdelta)
        #listdelta = np.nan_to_num(listdelta)

        print('listdelta', listdelta)

    # fi proves

    if request.method == 'GET':
        return render(request, 'proves.html', {
            'standingsB': stndB,
            'standingsC': stndC,
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
            'nicks': nicks,
            'delta1': delta1,
            'delta2': delta2,
            'delta3': delta3,
            'delta4': delta4,
            'delta5': delta5,
            })
    
def proves2(request):
        
    print('Proves2')

    currentedition = 34
    uri = 'https://api.football-data.org/v4/competitions/2001/matches/'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }
    response_matches = requests.get(uri, headers=headers)
    print('rsp matches', response_matches.json())
    partits = response_matches.json()['matches']
    print('partits', partits[:10])
#    partit = partits['area'].get('name')
#    print('partit', partit[:10])

    uri = 'https://api.football-data.org/v4/competitions/2001/teams/'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }
    response_teams = requests.get(uri, headers=headers)
#    print('rsp teams', response_teams.json())
    equips = response_teams.json()['teams']
#    print('equips', equips)

    uri = 'https://api.football-data.org/v4/competitions/2001/standings?standingType=TOTAL'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }
    response_groups = requests.get(uri, headers=headers)
#    print('rsp groups', response_groups.json())
    grups = response_groups.json()['standings']
#    print('grups', grups)

    teams = Teams.objects.all()
#    .annotate(grp=(('points'),filter=Q(items__dates__lt=data)),grp=F('grupsf_email__p_fname'),)
    teamsdb = Teamsdb.objects.all()
    fixtures = Fixtures.objects.all()

#    matches = response.json()['teams']
#    print(json.dumps(matches, indent=4, sort_keys=True))

#    test top scorer
    uri = 'https://api.football-data.org/v4/competitions/2018//scorers/'
    headers = { 'X-Auth-Token': '3d6936d5fb044a3b925f7a9383b7d4d6' }
    response_scorers = requests.get(uri, headers=headers)
    print('rsp scorers', response_scorers.json())
    scorers = response_scorers.json()['scorers']
    print('scorers', scorers[:10])


    if request.method == 'GET':
        return render(request, 'proves2.html', {
            'match': partits,
            'teams':teams,
            'teamsdb':teamsdb,
            'fictures': fixtures,
            'equips': equips,
            'grups': grups,
            'scorers': scorers,
        })