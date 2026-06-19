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

    currentedition = 37
    activeeditions = Editions.objects.filter(is_active=1)
    activeeditions2 = activeeditions.values()
    activeeditions3 = activeeditions.values_list()
    print('activeeditions', activeeditions[0])
    print('activeeditions2', activeeditions2[0])
    print('activeeditions3', activeeditions3[0])

    if request.method == 'GET':
        print('GET', 'player', pid)
        playerDBinfo = PlayerDB.objects.get(id=pid)
        formDB = PlayerDBInfoForm(instance=playerDBinfo)
        #        form = PlayerInfoForm(instance=playerinfo)    ----> move to under playerinfo

        try:
            playerinfo = Players.objects.get(playerdb=pid, editions=currentedition)
            print('playerinfo', playerinfo)
        except ValueError as error:
            print('Value error', error)
            playerinfo = None
        except TypeError as error:
            print('TypeError', error)
            return redirect('index.html')
        except Exception as error:
            print('if except: ', error)
            playerinfo = None


        if(playerinfo is None):
            edition = Editions.objects.filter(is_active=1)
        else:
            edition = None

        print(playerDBinfo)
        return render(request, 'playerinfo.html', {
            'playerDB': playerDBinfo,
            'player': playerinfo,
            'formDB': formDB,
            'pid': pid,
            'editionform': EditionsForm,
            'editions': edition
        })

    else:
        print('POST')
        try:
            print(request.POST)
            newedition = Editions.objects.get(id=request.POST['e_id'])
            userDB = PlayerDB.objects.get(id=pid)
            user = Players.objects.get(playerdb=userDB, editions=currentedition)
            print(pid, newedition, userDB, user)
            print('user registered')
            playerid = user.id
            return redirect('game')


        except:
            print('new player joined')
            newuser = Players.objects.create(playerdb=userDB, p_fname=userDB.fname, p_lname=userDB.lname, p_email=userDB.email, ppsw="void", winnable=1, editions=newedition)
            newuser.save()
            playerid = newuser.id
            return redirect('game')

def about(request):

    if request.method == 'GET':
        print('enviando formulario Login')
        return render(request, 'about.html', {
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
            return render(request, 'about.html', {
                'form': PlayerDBLogForm,
                'error': 'Email not found'
            })

#--------------
# New developments ElJoc5.0
#--------------

def access5(request):

    if request.method == 'GET':
        print('GET')
        return render(request, 'access5.html')
    
    email = request.POST['email']
    print('email: ', email)

    try:
        print('access5 ok')
        user = PlayerDB.objects.get(email=email)
        print('access5 ok 2', user.id)
        request.session["playerdb_id"] = user.id
        request.session["player_email"] = user.email
        return redirect('playerinfo5', pid=user.id)
    
    except PlayerDB.DoesNotExist:
        print('access5 ko')
        return redirect(f'/register/?email={email}')

def register5(request):

    if request.method == 'GET':
        email = request.GET.get('email', '')
        return render(
            request,
            'register5.html',
            {
            'email': email
            }
        )
    else:
        try:
            user = PlayerDB.objects.get(email=request.POST['email'])
            print('existing email')
            return render(
                request,
                'register5.html',
                {
                    'error': 'Email already in use',
                    'email': request.POST['email']
                }
            )

        except PlayerDB.DoesNotExist:
            newuser=PlayerDB.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email']
                )

            newuser.save()
            request.session["playerdb_id"] = newuser.id
            request.session["player_email"] = newuser.email
            print('user registered')
            return redirect('playerinfo5', pid=newuser.id)

def playerinfo5(request, pid):

    playerDBinfo = PlayerDB.objects.get(id=pid)
    request.session["playerdb_id"] = playerDBinfo.id
    request.session["player_email"] = playerDBinfo.email
    active_editions = Editions.objects.filter(is_active=1)

    edition_cards = []

    for edition in active_editions:
        player = Players.objects.filter(
            playerdb=playerDBinfo,
            editions=edition
        ).first()

        edition_cards.append({
            'edition': edition,
            'player': player,
            'is_joined': player is not None
        })

    if request.method == 'GET':
        return render(request, 'playerinfo5.html', {
            'playerDB': playerDBinfo,
            'pid': pid,
            'edition_cards': edition_cards
        })

    else:
        edition_id = request.POST['edition_id']
        edition = Editions.objects.get(id=edition_id)

        existing_player = Players.objects.filter(
            playerdb=playerDBinfo,
            editions=edition
        ).first()

        if existing_player is None:
            Players.objects.create(
                playerdb=playerDBinfo,
                p_fname=playerDBinfo.fname,
                p_lname=playerDBinfo.lname,
                p_email=playerDBinfo.email,
                ppsw="void",
                winnable=1,
                editions=edition
            )
        else:
            player = existing_player

        request.session["player_id"] = player.id
        request.session["edition_id"] = edition.id
        request.session["player_email"] = playerDBinfo.email

        return redirect('game')
