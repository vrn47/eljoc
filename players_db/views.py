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
        print('enviando formulario about')
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

def history(request):

    if request.method == 'GET':
        print('enviando formulario history')
        return render(request, 'history.html', {
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
            return render(request, 'history.html', {
                'form': PlayerDBLogForm,
                'error': 'Email not found'
            })

#--------------
# New developments ElJoc5.0
#--------------

def build_username(fname, lname):
    """
    Build El Joc username.

    Rule:
    - First letter of first name in uppercase
    - Full last name with first letter uppercase

    Example:
    Víctor Roig -> VRoig
    """
    return fname[0].upper() + lname.capitalize()

def access5(request):

# Access page

    """
    GET: Shows the access form.

    POST:
    - Looks for an existing PlayerDB by email.
    - If found, stores basic player data in session.
    - Redirects to playerinfo5.
    - If not found, redirects to register5 with email prefilled.
    """

    print('access5')

    if request.method == 'GET':
        print('GET')
        return render(request, 'access5.html')
    
    email = request.POST['email'].strip().lower()
    request.session["eljocsession_player_email"] = email
    print('email: ', email)

    try:
        print('try')
        user = PlayerDB.objects.get(email=email)
        print('access5 ok 2', user.id)

        # Store global player identity in session.
        # This is available before choosing an edition.
        request.session["eljocsession_playerdb_id"] = user.id
        request.session["eljocsession_player_email"] = user.email
        request.session["eljocsession_username"] = build_username(user.fname, user.lname)

        return redirect('playerinfo5')

    except PlayerDB.DoesNotExist:
        print('try ko')
        return redirect(register5)

def register5(request):

    """
    Register page.

    GET:
    - Shows the registration form.
    - If the user came from access5, the email can be prefilled.

    POST:
    - Checks whether the email already exists in PlayerDB.
    - If it exists, shows an error.
    - If it does not exist, creates a new PlayerDB record.
    - Stores player identity data in session.
    - Redirects to playerinfo5.
    """

    print('register5')

    # 01 GET: show register form.

    if request.method == 'GET':
        print('GET')
        eljoctemp_email = request.session.get('eljocsession_player_email')
        return render(
            request,
            'register5.html',
            {
            'email': eljoctemp_email
            }
        )
    else:
        # 02 POST: get form info.
        print('POST')
        try:
            # 03 Check if email already exists and show error if it does
            PlayerDB.objects.get(email=request.POST['email'])
            print('existing email')
            return render(request, 'register5.html',{
                    'error': 'Email already in use',
                    'email': request.POST['email']
            })

        # 04 If email does not exist, create new PlayerDB record from form info.
        except PlayerDB.DoesNotExist:
            eljoctemp_PDB = PlayerDB.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email']
                )
            # eljoctemp_PDB.save() it seems redundant
            print('newuser registered')

            # 05 Store global player identity in session.
            request.session["eljocsession_playerdb_id"] = eljoctemp_PDB.id
            request.session["eljocsession_player_email"] = eljoctemp_PDB.email
            request.session["eljocsession_username"] = build_username(eljoctemp_PDB.fname, eljoctemp_PDB.lname)
            return redirect('playerinfo5')

def playerinfo5(request):

    print('playerinfo5')

    # verificació de sessió oberta via get() perquè, si la clau no existeix, retorna None en lloc de provocar un KeyError.
    session = request.session.get("eljocsession_playerdb_id")
    if session is None:
        # Eliminem qualsevol resta d'una sessió incompleta.
        request.session.flush()
        # Tornem l'usuari a la pàgina d'accés.
        return redirect("access5")
    # fi verificació de sessió

    """
    Player info page.

    Get information and values:
    - Player DB id
    - Player email
    - Username

    GET:
    - Shows player database info.
    - Shows active editions.
    - Shows whether the player has already joined each edition.

    POST:
    - Player can join an edition.
    - If player already exists for that edition, reuse it.
    - Store game session data:
        player_id
        edition_id
        player_email
        username
    - Redirect to game.
    """

    # 01 Get data from session.
    eljoctemp_DBid = request.session.get("eljocsession_playerdb_id")

    
    # 02 If there is no session, the user must access again.
    if eljoctemp_DBid is None:
        request.session.flush()
        return redirect("access5")
    
    # 03 Retrive player details from DB.
    eljoctemp_PDB = PlayerDB.objects.get(id=eljoctemp_DBid)
    print(eljoctemp_PDB)

    # 04 Build active edition cards
    active_editions = Editions.objects.filter(is_active=1)
    edition_cards = []

    for edition in active_editions:
        eljoctemp_player = Players.objects.filter(
            playerdb=eljoctemp_PDB,
            editions=edition
        ).first()

        edition_cards.append({
            'edition': edition,
            'player': eljoctemp_player,
            'is_joined': eljoctemp_player is not None
        })

    # 05 GET: show player info page

    if request.method == 'GET':
        print('GET')
        return render(request, 'playerinfo5.html', {
            'playerDB': eljoctemp_PDB,
            'edition_cards': edition_cards
        })

    # 06 POST: player selects an edition

    else:
        print('POST')
    
        # Get selected edition from form.
        edition = Editions.objects.get(id=request.POST['edition_id'])

        # Check whether this PlayerDB already has a Players record for the selected edition.
        eljoctemp_player = Players.objects.filter(
            playerdb=eljoctemp_PDB,
            editions=edition
        ).first()

        # If the player is not joined yet, create the Players record.
        if eljoctemp_player is None:
            eljoctemp_player = Players.objects.create(
                playerdb=eljoctemp_PDB,
                p_fname=eljoctemp_PDB.fname,
                p_lname=eljoctemp_PDB.lname,
                p_email=eljoctemp_PDB.email,
                ppsw="void",
                winnable=1,
                editions=edition
            )

    # 07 Add game session data (edition and playerID)

        request.session["eljocsession_player_id"] = eljoctemp_player.id
        request.session["eljocsession_edition_id"] = edition.id
        request.session["eljocsession_edition_name"] = edition.name
        request.session["eljocsession_edition_short"] = edition.short

    # 08 Enter game

        return redirect('game')

def logout(request):
    request.session.flush()
    return redirect("access5")