import requests,json
import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pages.models import Game
from pages.psw import generatepsw, psw_length

from globals.toolkit import getRequestIP,getCookieData

#This return the login page
def login(request):
    return render(request, "login.html", {"psw":generatepsw(16)})
    
def getRoomList(roomname=None):
    id=[]
    name=[]
    occupancy=[]

    if roomname is None:
        games = Game.getActiveRooms()
    else:
        games = Game.getActiveRooms(roomname=roomname)

    for game in games:
        if not game.isExpired():
            id.append(game.id)
            name.append(game.roomname)
            occupancy.append('2/2' if len(game.names[1])>0 else '1/2')
    return id, name, occupancy

#This return the lobby page
def lobby(request):
    id,name,occupancy=getRoomList()
    return render(request, "lobby.html", {"ids":id, "names":name, "occupancy":occupancy})


def getallrooms(request):
    id,name,occupancy=getRoomList()
    return HttpResponse(json.dumps({"name":name, "id":id, "occupancy":occupancy}))
    
def searchrooms(request):
    roomname = request.GET.get('name')
    print(roomname)
    id,name,occupancy=getRoomList(roomname)
    return HttpResponse(json.dumps({"name":name, "id":id, "occupancy":occupancy}))
    
def room(request, id):
    
    games = Game.getActiveRooms(id=id) # ==============================================================================
    if not len(games)==1:
        return HttpResponse("Either no such room nor multiple room detected!")
    game = games[0]
    
    # retrive information from the cookie
    roomid, name, mypsw = getCookieData(request)
    ip = getRequestIP(request)

    order = game.checkIdenttity(roomid, name, mypsw)

    if order<=0:
        reg = game.registerPlayer(name, ip, mypsw)
        order = game.checkIdenttity(roomid, name, mypsw)
    
    return render(request, "gameroom.html", {"id":id, "roomname":game.roomname, "p1_name":game.names[0], "p2_name":game.names[1], "order":order})
    
def db(request):
    games = Game.objects.all()
    
    return render(request, "db.html", {"games": games})
    
def create(request):
    name = request.GET.get('name')
    game = Game.create(name)
    if game is not None:
        game.save()
        print("Game room %s(%d) created!"%(game.roomname, game.id))
        return HttpResponse(json.dumps({"id":game.id}))
    else:
        return HttpResponse(json.dumps({"msg":''}))


def resetrooms(request):
    games=Game.getActiveRooms()
    
    for game in games:
        game.deactivate()
    
    return HttpResponse("Cleared!")
