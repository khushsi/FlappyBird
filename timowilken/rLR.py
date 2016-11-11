#Qlearning
import pickle
import random

grid=4
gamma=0.7
alpha=0.7
WIN_WIDTH = 284 * 2     # BG image size: 284x512 px; tiled twice
WIN_HEIGHT = 512

class gameState:

    def __init__(self):
        self.statespacemap = getStateSpace()
        self.rewardMap = getRewardMap()
        self.visitedMap = getVisitedMap()


    def getState(self,x,y):
        if (not self.statespacemap.has_key((x,y)) ):
            self.statespacemap[(x,y)] = (0,0)
           
        return self.statespacemap[(x,y)]

    def setStateValuebyaction(self,x,y,a,val):
        if (not self.statespacemap.has_key((x,y)) ):
            self.statespacemap[(x,y)] = (0,0)
        (flap,noflap) = self.statespacemap[(x,y)]
        if(a==1):
            self.statespacemap[(x,y)]= (val,noflap)
        else:
            self.statespacemap[(x,y)]= (flap,val)        
        
    def setStateValue(self,x,y,flap,noflap):
        self.statespacemap[(x,y)] = (flap,noflap)
        
    def getMaxVal(self,x,y):
        if (not self.statespacemap.has_key((x,y)) ):
            self.statespacemap[(x,y)] = (0,0)
           
        return max(self.statespacemap[(x,y)])

    def updateReward(self,ox,oy,cx,cy,a,val):
        if (not self.rewardMap.has_key((ox,oy,a,cx,cy)) ):
            self.rewardMap[(ox,oy,a,cx,cy)] = val

    def getReward(self,ox,oy,cx,cy,a):
        if not self.rewardMap.has_key((ox,oy,a,cx,cy) ):
            self.rewardMap[(ox,oy,a,cx,cy)] = 0
           
        return self.rewardMap[(ox,oy,a,cx,cy)]
           
        
    def getNextAction(self,cx,cy):
        if((cx,cy,1) not in self.visitedMap):
            print "not visited"
            self.visitedMap.append((cx,cy,1))
            return 1
        elif((cx,cy,1) not in self.visitedMap):
            self.visitedMap.append((cx,cy,0))
            return 0
        
        (flap,noflap) = self.getState(cx, cy)
        if(flap == noflap):
            return random.randrange(0,2)
        if(flap > noflap):
            return 1
        else:
            return 0        

    def updateQ(self,ox,oy,a,cx,cy):
        (flap,noflap) = self.getState(ox, oy)
        qsample_sa = self.getReward(ox, oy, cx, cy, a)  + gamma * self.getMaxVal(cx, cy)
        if a == 1:
            flap = round(flap + alpha * (qsample_sa - flap))
        else:
            noflap = round(noflap + alpha * (qsample_sa - noflap))
        #print(ox,oy,flap,noflap,cx,cy)
        self.setStateValue(ox, oy, flap, noflap)    
        
        
def getStateSpace():
    windowdivval = 1
    spacelist = dict() 
    try:
        spacelist = pickle.load( open( "stateMapR.pickle", "rb" ) )
    except:
        print "no statemap generated yet"
    return spacelist 

def getVisitedMap():
    
    visitedlist = [] 
    try:
        visitedlist = pickle.load( open( "visitedMapR.pickle", "rb" ) )
    except:
        print "no statemap generated yet"
    return visitedlist 

def getRewardMap():
    rewardlist = dict() 
    try:
        rewardlist = pickle.load( open( "rewardMapR.pickle", "rb" ) )
    except:
        print "no reward generated yet"
    return rewardlist 

