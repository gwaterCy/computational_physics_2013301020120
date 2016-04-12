# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 18:30:15 2016
solve the problem of calculating cannon initial velocity to attack a given target
@author: yi cao
"""
from matplotlib.pyplot import *
from matplotlib import animation
import math

g = 9.8
b2m = 4*1e-5
Origin = [0.,0.]
Target = [20000.,1000.]
Error_limit = 0.1

class flight_state:
    def __init__(self, _x = 0, _y = 0, _vx = 0, _vy = 0, _x1 = 0,_y1 = 0,_t = 0):
        self.x = _x
        self.y = _y
        self.vx = _vx
        self.vy = _vy
        self.end_x= _x1
        self.end_y = _y1
        self.t = _t

class cannon:
    def __init__(self, _fs = flight_state(0, 0, 0, 0, 0, 0, 0), _dt = 0.1):
        self.cannon_flight_state = []
        self.cannon_flight_state.append(_fs)
        self.dt = _dt
        # print self.cannon_flight_state[-1].x, self.cannon_flight_state[-1].y, self.cannon_flight_state[-1].vx, self.cannon_flight_state[-1].vy

    def next_state(self, current_state):
        global g
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)

    def shoot(self):
        end_y = self.cannon_flight_state[0].end_y
        while not(self.cannon_flight_state[-1].y < end_y and self.cannon_flight_state[-1].vy < 0):
            self.cannon_flight_state.append(self.next_state(self.cannon_flight_state[-1]))
            #print self.cannon_flight_state[-1].x, self.cannon_flight_state[-1].y, self.cannon_flight_state[-1].vx, self.cannon_flight_state[-1].vy
        
        r = - (self.cannon_flight_state[-2].y-end_y) / (self.cannon_flight_state[-1].y-end_y)
        self.cannon_flight_state[-1].x = (self.cannon_flight_state[-2].x + r * self.cannon_flight_state[-1].x) / (r + 1)
        self.cannon_flight_state[-1].y = end_y
        print self.cannon_flight_state[-1].x, self.cannon_flight_state[-1].y, self.cannon_flight_state[-1].vx, self.cannon_flight_state[-1].vy
        return self.cannon_flight_state     
        
    def show_trajectory(self):
        x = []
        y = []
        for fs in self.cannon_flight_state:
            x.append(fs.x)
            y.append(fs.y)
        figure(figsize=(10,6))
        plot([0,self.cannon_flight_state[0].end_x*1.2],[self.cannon_flight_state[0].end_y,self.cannon_flight_state[0].end_y],color='blue',linewidth='2',linestyle='--')
        plot([self.cannon_flight_state[0].end_x,self.cannon_flight_state[0].end_x],[0,self.cannon_flight_state[0].end_y*1.2],color='blue',linewidth='2',linestyle='--')        
        plot(x,y,color='red')
        xlabel('distance(m)')
        ylabel('height(m)')
        #show()

class Drag_cannon(cannon):
    def next_state(self, current_state):
        global g, b2m
        v = math.sqrt(current_state.vx * current_state.vx + current_state.vy * current_state.vy)
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx - b2m * v * current_state.vx * self.dt
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt - b2m * v * current_state.vy * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)

def simulation(v):
    global Target,Origin
    drag_cannon = Drag_cannon(flight_state(Origin[0], Origin[1], v, v,Target[0],Target[1], 0),_dt=0.1)
    a = drag_cannon.shoot()
    return a
    
    
def scanning():
    global Target,Origin,Error_limit
    v = sqrt((Target[0]-Origin[0])**2*g*0.5/(Target[0]-Origin[0]-Target[1]+Origin[1]))
    dl = Target[0]-simulation(v)[-1].x
    while(dl>Error_limit):
        ScanSpeed = max((dl/100)**2/100,0.01)
        v = v +ScanSpeed
        dl = Target[0]-simulation(v)[-1].x
        print 'v:'+str(v)
    print 'v:'+str(v)
    return v
    
fig = figure(figsize=(8,6))
ax = axes(xlim=(0, 25000), ylim=(0, 8000))
ax.plot([0,Target[0]*1.2],[Target[1],Target[1]],color='r',linewidth='2',linestyle='--')
ax.plot([Target[0],Target[0]],[0,Target[1]*1.2],color='r',linewidth='2',linestyle='--') 
v = math.sqrt((Target[0]-Origin[0])**2*g*0.5/(Target[0]-Origin[0]-Target[1]+Origin[1]))   
line, = ax.plot([], [], lw=2)
sign = -20
_x,_y =[],[]
def init():
    line.set_data([], [])
    return line,
    
def animate(i):
    global Target,Origin,Error_limit,v,sign,_x,_y
    x = []
    y = []    
    if sign<-1:
        sign = sign + 1
    elif sign == -1:
        flight_state = simulation(v)
        for i in flight_state:
            x.append(i.x)
            y.append(i.y)
        dl = Target[0]-flight_state[-1].x
        if (dl>Error_limit):
            ScanSpeed = max((dl/5000),0.05)
            v = v +ScanSpeed
        else:
            sign = 0
    else:
        flight_state = simulation(v)
        try:
            _x.append(flight_state[sign].x)
            _y.append(flight_state[sign].y)
            x, y = _x,_y
            sign = sign +1 
            print sign
        except IndexError:
            exit()         
    line.set_data(x, y)
    return line,
    
anim = animation.FuncAnimation(fig, animate, init_func=init,frames=200, interval=20, blit=True)
show()         
