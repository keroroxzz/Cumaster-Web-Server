import numpy as np
import json
import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField

from globals.toolkit import getRequestIP,getCookieData
from pages.psw import generatepsw, psw_length

# Game board related parameters
pattern_size = 5
board_size = 19
default_board = '0'*(board_size*board_size)

# Name length
room_name_length = 10
player_name_length = 16

# The patteren of dick
patterns=[
		[[0,0],[1,0],[2,0],[3,-1],[3,1]],
		[[0,0],[1,1],[2,2],[3,2],[2,3]],
		[[0,0],[0,1],[0,2],[-1,3],[1,3]],
		[[0,0],[-1,1],[-3,2],[-2,2],[-2,3]],
		[[0,0],[-1,0],[-3,-1],[-3,1],[-2,0]],
		[[0,0],[-1,-1],[-3,-2],[-2,-3],[-2,-2]],
		[[0,0],[0,-1],[-1,-3],[1,-3],[0,-2]],
		[[0,0],[1,-1],[2,-2],[3,-2],[2,-3]]]

# Datetime timezone
tz = datetime.timezone(datetime.timedelta(0))

# This is the table for game room that contain all the information about the player and the game.
class Game(models.Model):

    # room data
    status = models.PositiveSmallIntegerField(default=0)
    roomname = models.CharField(max_length=room_name_length, default='新房間')

    # player data
    names = ArrayField(models.CharField(max_length=player_name_length, default=''), size=2)
    IPs = ArrayField(models.CharField(max_length=16, default=''), size=2)
    passwords = ArrayField(models.CharField(max_length=psw_length, default=''), size=2)
    scores = ArrayField(models.PositiveSmallIntegerField(default=0), size=2)
    
    # game data
    lastupdate = models.DateTimeField("date created", auto_now_add=True)
    lastrequest = models.DateTimeField("last_request", auto_now_add=True)
    step = models.IntegerField(default=-1)  #-1 means haven't begun
    lastmove = models.CharField(max_length=128, blank=True, default='')   # Formate:'{player id,x,y,type}'
    board = models.CharField(max_length=board_size*board_size, blank=True, default=default_board)
    
    # This method is for creating and initializing a new Game instance.
    @classmethod
    def spawn(clf, id):

        newgame = clf()
        newgame.id=id
        newgame.passwords = ['','']
        newgame.names = ['','']
        newgame.IPs = ['','']
        newgame.scores = [0, 0]
        newgame.lastupdate = datetime.datetime.now(tz)
        newgame.lastrequest = datetime.datetime.now(tz)
        newgame.save()
        
        return newgame

    # This method is for creating and initializing a new Game instance.
    @classmethod
    def create(clf, name):

        # Prepare 50 empty rooms
        allrooms = clf.objects.all()
        lastid=0
        if(len(allrooms)>0):
            lastid = allrooms.last().id
        for i in range(0,50-len(allrooms)):
            clf.spawn(i+lastid)

        validrooms = clf.objects.filter(status=0)

        if len(validrooms)>0:
            room = validrooms[0]
            room.activate(name)
            return room
        
        return None

    def activate(self, newname):
        self.roomname = newname
        self.status = 1
        self.passwords = ['','']
        self.names = ['','']
        self.IPs = ['','']
        self.scores = [0, 0]
        self.step=-1
        self.lastmove=''
        self.board=default_board
        self.lastupdate = datetime.datetime.now(tz)
        self.lastrequest = datetime.datetime.now(tz)
        self.save()

    def deactivate(self):
        self.status = 0
        self.save()

    @classmethod
    def getActiveRooms(clf, roomname=None, id=None):
        if roomname is not None and id is not None:
            return clf.objects.filter(status=1, roomname=roomname, id=id)
        elif roomname is not None:
            return clf.objects.filter(status=1, roomname=roomname)
        elif id is not None:
            return clf.objects.filter(status=1, id=id)
        else:
            return clf.objects.filter(status=1)

    def isActive(self):
        return self.status>0 and self.status<3

    # register a new player
    def registerPlayer(self, name, ip, psw):

        if not self.isActive():
            return False

        # Get the order of the player
        id=-1
        if len(self.passwords[0])==0:
            id=0
        elif len(self.passwords[1])==0:
            id=1
        else:
            return False

        # Check if the name or psw are identical to the existing player
        if id==1 and (name == self.names[0] or psw == self.passwords[0]):
            return False

        print('%s(%s) just registed as a player in room %d.'%(name, ip, self.id))
        self.names[id]=name
        self.IPs[id]=ip
        self.passwords[id]=psw

        # The second player get in.
        if id==1:
            self.step = 0
            print('All players are in, ready to start room %d.'%(self.id))

        # Update the late update time
        self.lastupdate = datetime.datetime.now(tz)

        self.save()
        return True

    # check if the request was from a player, and return the order of the player 
    def checkIdenttity(self, id, name, psw):

        # let's check the target room id first
        if not id==self.id or not self.isActive():
            return -1

        # then check the identity
        if name==self.names[0] and psw==self.passwords[0]:# and ip==self.IPs[0]:
            return 1
        elif name==self.names[1] and psw==self.passwords[1]:# and ip==self.IPs[1]:
            return 2
        return 0

    def getCurrentPlayer(self):
        return (max(self.step, 0)%2) + 1

    def currentColor(self, who):
        color = self.getCurrentPlayer()
        if who==1 and color==1:
            return '1'
        elif who==2 and color==2:
            return '2'
        else:
            return False
    
    def placeOne(self, playerid, x, y):
        # Check the availablility of the action
        if x<0 or x>18 or y<0 or y>18:
            return False

        if self.isGameOver() or not self.hasBegun():
            return False
            
        # Check player identity and decide the color
        color = self.currentColor(playerid)
        if color==False:
            return False

        # Update the late update time
        self.lastupdate = datetime.datetime.now(tz)

        # update the board
        if self.setStone(x, y, color):
            self.lastmove = json.dumps({"msg":'step', "p":playerid, "x":x, "y":y, "c":color})
            self.step += 1
            self.save()
            return True
        else:
            return False

    # calculate the left time
    def getLeftTime(self):
        now = datetime.datetime.now(tz)
        exp = now - self.lastupdate
        exp_sec = exp.total_seconds()

        return min(62-exp_sec, 60)  # Extra 2 sec for update compensation, because I'm lazy to deal with that issue

    # calculate the left time for waiting connection
    def getConnectionTimeOut(self):
        now = datetime.datetime.now(tz)
        exp = now - self.lastrequest
        exp_sec = exp.total_seconds()

        return max(0, exp_sec-1)
        
    def isExpired(self):
        timeout = self.getConnectionTimeOut()
        if timeout>20 or (self.hasBegun() and self.getLeftTime()<0):
            self.deactivate()
            print("Room expired!! Deactivate this room!")
            return True
        return False

    def isWaiting(self):
        return self.status==1 and self.step==-1

    def hasBegun(self):
        return self.status==1 and self.step>-1

    def isGameOver(self):
        return not(self.scores[0]<5 and self.scores[1]<5)

    def getState(self):
        return json.dumps({"msg":'init', "names":self.names, "step":self.step})

    def getBoard(self):
        return json.dumps({"msg":'all', "step":self.step, "board":self.board, "scores":self.scores})

    def getStone(self, x, y):
        if x<0 or x>18 or y<0 or y>18:
            return -1
        return self.board[x+y*board_size]

    def setStone(self, x, y, color):
        if (self.board[x+y*board_size]=='0' and not color=='0') or (not self.board[x+y*board_size]=='0' and color=='0'):
            self.board=self.board[:x+y*board_size]+color+self.board[x+y*board_size+1:]
            return True
        else:
            return False

    def checkDick(self, x, y, d, cum, color):
        pat = patterns[d]
        for i in range(5):
            if not self.getStone(x+pat[i][0], y+pat[i][1])==color:
                return False
        
        opposite = '1' if color=='2' else '2'
        for i in range(cum):
            if not self.getStone(x-pat[1][0]*(i+1), y-pat[1][1]*(i+1))==opposite:
                return False

        return True

    def pickDick(self, playerid, x, y, d, cum):

        # Check player identity and decide the color
        color = self.currentColor(playerid)
        if color==False:
            return False

        if self.isGameOver():
            return False

        if self.checkDick(x, y, d, cum, color):
            
            # Remove the stones
            pat = patterns[d]
            for i in range(5):
                self.setStone(x+pat[i][0], y+pat[i][1], '0')

            for i in range(cum):
                self.setStone(x-pat[1][0]*(i+1), y-pat[1][1]*(i+1), '0')

            self.scores[playerid-1]+=cum

            # Update the last update time
            self.lastupdate = datetime.datetime.now(tz)

            self.lastmove = json.dumps({"msg":'pick', "p":playerid, "x":x, "y":y, "d":d, "c":cum, "scores":self.scores})
            self.step+=1
            self.save()
            return True
        
        return False

    # update the time stamp of the latest request from player
    def updateReqTime(self, id, name, psw):
        if self.checkIdenttity(id, name, psw)==self.getCurrentPlayer():
            self.lastrequest = datetime.datetime.now(tz)
            self.save()

    def updateRequest(self, gamestep, name=None, psw=None):
        response = ''

        self.updateReqTime(self.id, name, psw)
        timeout = self.getConnectionTimeOut()

        # Aquire the game data
        if self.step == gamestep:
            if not self.hasBegun():
                return ''
            elif timeout>0:
                response = "{\"msg\": \"timeout\", \"time\": %d}"%(timeout)
            else:
                response = "{\"msg\": \"time\", \"time\": %d}"%(self.getLeftTime())
            
        elif self.step==gamestep+1: # If the client need update
            if self.step<=0: # If the game is not started yet
                response = self.getState()
            else:
                response = self.lastmove
        else:
            #return the whole board and the step
            response = self.getBoard()

        # Check expiration
        self.isExpired()

        return response