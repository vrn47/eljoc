from django.shortcuts import render, redirect, HttpResponse
from .models import Items, Fixtures, Teams, Teamsdb, Forecasts, Players
from .forms import ItemsForm, ForecastsForm, PlayersForm
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.db.models import Sum, Count
from array import *
import numpy as np

import requests
import json

# Create your views here.

def game(request):
        return render(request, 'game.html')

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

    players = Players.objects.all()
    ppoints = Forecasts.objects.values('f_email').annotate(pts=Sum('points')).order_by('-pts')
    standings = list(ppoints.values_list('f_email', flat=True))
    print(standings, ppoints, players)
    names = []
    initial = []
    surnames = []
    for x in standings:
        names.append(list(players.filter(p_email=x).values_list('p_fname', flat=True)))
        for y in names:
            for z in y:
                for w in z:
                    break
        initial.append(w)
        surnames.append(list(players.filter(p_email=x).values_list('p_lname', flat=True)))
    surnames_np = np.array(surnames)
    surnames_np = surnames_np.transpose()
    initials_np = np.array(initial)
    initials_np = [initials_np]
    nicks = np.char.add(initials_np, surnames_np)
    standings = [standings]
    standings.append(list(ppoints.values_list('pts', flat=True)))
    stndings_np = np.array(standings)
    stndings_np = np.concatenate((stndings_np, nicks), axis=0)
   
    stndings_np = stndings_np.transpose()
    print (stndings_np)
    if request.method == 'GET':
        print('enviando formulario forecast')
        return render(request, 'standings.html', {
            'roig': stndings_np
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