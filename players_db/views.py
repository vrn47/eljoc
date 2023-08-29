from django.shortcuts import render, redirect
from .models import Players, PlayerDB, Editions
from .forms import PlayerDBLogForm, PlayerDBInfoForm, PlayerInfoForm, EditionsForm
from django.contrib.auth import login, logout, authenticate


# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):

    if request.method == 'GET':
        print('enviando formulario Login')
        return render(request, 'login.html', {
            'form': PlayerDBLogForm
        })
    else:
        print('request: ', request)
        print('request.POST:', request.POST)
        print("request.POST['email']: ", request.POST['email'])
        print('obteniendo datos')
        try:
            user = PlayerDB.objects.get(email=request.POST['email'])
            print('ok')
            print(user)
            print(user.id)
            playerid = user.id
            print(playerid)
            return redirect('playerinfo', pid=playerid)

        except:
            print('ko')
            return render(request, 'login.html', {
                'form': PlayerDBLogForm,
                'error': 'Email not found'
            })

def register(request):

    if request.method == 'GET':
        return render(request, 'register.html', {
            'form': PlayerDBLogForm
        })
    else:
        try:
            user = PlayerDB.objects.get(email=request.POST['email'])
            print('existing email')
            return render(request, 'register.html', {
                'form': PlayerDBLogForm,
                'error': 'Email already in use'
            })

        except:
            newuser=PlayerDB.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'])
            newuser.save()
            playerid = newuser.id
            print('user registered')
            return redirect('playerinfo', pid=playerid)

def playerinfo(request, pid):

    if request.method == 'GET':
        print('GET')
        try:
            print('player')
            print(pid)
        #    print(request.POST['email'])
                
            playerDBinfo = PlayerDB.objects.get(id=pid)
            formDB = PlayerDBInfoForm(instance=playerDBinfo)

    #        playerinfo = Players.objects.get(playerdb=pid)
    #        form = PlayerInfoForm(instance=playerinfo)

            edition = Editions.objects.filter(is_active=1)

            print(playerDBinfo)
    #        print(playerinfo)
        #    return render(request, 'playerinfo.html')
            return render(request, 'playerinfo.html', {
                'playerDB': playerDBinfo,
    #            'player': playerinfo,
                'formDB': formDB,
    #            'form': form,
                'pid': pid,
                'editionform': EditionsForm,
                'editions': edition
            })
        
        except ValueError:
            print('Value error')
            return render(request, 'playerinfo.html', {
                'playerDB': playerDBinfo,
                'formDB': formDB,
                'pid': pid,
            })
        
        except TypeError:
            print('TypeError')
            return redirect('index.html')

        except Exception as error:
            print('if except: ', error)

    else:
        print('POST')
        try:
            print(request.POST)
            newedition = Editions.objects.get(id=request.POST['e_id'])
            userDB = PlayerDB.objects.get(id=pid)
            user = Players.objects.get(playerdb=userDB)
            print(pid, newedition, userDB, user)
            print('user registered')
            playerid = user.id
            return redirect('game')

        except:
            print('new player')
            newuser = Players.objects.create(playerdb=userDB, p_fname=userDB.fname, p_lname=userDB.lname, p_email=userDB.email, ppsw="void", winnable=1)
            newuser.save()
            playerid = newuser.id
            return redirect('game')
