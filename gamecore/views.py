import requests,json
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pages.models import Game
from globals.toolkit import getRequestIP,getCookieData

@csrf_exempt
def step(request):
    if not request.method == 'POST':
        return HttpResponse('')
        
    # get the args from url
    x = request.POST.get('x')
    y = request.POST.get('y')
    
    if x is None or y is None:
        return HttpResponse('')
        
    x = int(x)
    y = int(y)
    roomid, playername, psw = getCookieData(request)

    games = Game.getActiveRooms(id=roomid)
    
    # suppose that the id should be identical, but just to ensure
    if not len(games)==1:
        return HttpResponse('')
    
    game = games[0]
    playerid = game.checkIdenttity(roomid, playername, psw)
    if playerid<=0:
        return HttpResponse('')

    if game.placeOne(playerid, x, y):
        return HttpResponse('')
    else:
        return HttpResponse('')
        
# This function handle the dick picking processing
@csrf_exempt
def pick(request):
    if not request.method == 'POST':
        return HttpResponse('')
        
    # get the args from url
    x = request.POST.get('x')
    y = request.POST.get('y')
    direction = request.POST.get('d')
    cum = request.POST.get('cum')
    
    if x is None or y is None:
        return HttpResponse('')
        
    x = int(x)
    y = int(y)
    direction = int(direction)
    cum = int(cum)

    roomid, playername, psw = getCookieData(request)
    games = Game.getActiveRooms(id=roomid)
    
    if not len(games)==1:
        return HttpResponse('')

    game = games[0]
    playerid = game.checkIdenttity(roomid, playername, psw)
    if playerid<=0:
        return HttpResponse('')

    game.pickDick(playerid, x, y, direction, cum)
    return HttpResponse('')
        
def update(request):
    if not request.method == 'GET':
        return HttpResponse('')
        
    gamestep = request.GET.get('step')
    
    if gamestep is None:
        return HttpResponse('')

    gamestep = int(gamestep)
    roomid, playername, psw = getCookieData(request)
    games = Game.getActiveRooms(id=roomid)
    
    if not len(games)==1:
        return HttpResponse('')

    game = games[0]

    return HttpResponse(game.updateRequest(gamestep, name=playername, psw=psw))