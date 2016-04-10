# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 18:30:15 2016
solve the problem of calculating cannon initial velocity to attack a given target
@author: yi cao
"""
from pylab import *
from matplotlib import pyplot as plt

g = 9.8
b2m = 4*1e-5
Origin = [0.,0.]
Target = [10000.,1000.]
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
        figure(figsize(10,6))
        plot([0,self.cannon_flight_state[0].end_x*1.2],[self.cannon_flight_state[0].end_y,self.cannon_flight_state[0].end_y],color='blue',linewidth='2',linestyle='--')
        plot([self.cannon_flight_state[0].end_x,self.cannon_flight_state[0].end_x],[0,self.cannon_flight_state[0].end_y*1.2],color='blue',linewidth='2',linestyle='--')        
        plot(x,y,color='red')
        xlabel('distance(m)')
        ylabel('height(m)')
        savefig('123.png')
        #show()

class Drag_cannon(cannon):
    def next_state(self, current_state):
        global g, b2m
        v = sqrt(current_state.vx * current_state.vx + current_state.vy * current_state.vy)
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx - b2m * v * current_state.vx * self.dt
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt - b2m * v * current_state.vy * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)

def simulation(v):
    global Target,Origin
    drag_cannon = Drag_cannon(flight_state(Origin[0], Origin[0], v, v,Target[0],Target[1], 0),_dt=0.1)
    a = drag_cannon.shoot()
    return a
    
    
def scanning():
    global Target,Origin,Error_limit
    v = sqrt((Target[0]-Origin[0])**2*g*0.5/(Target[0]-Origin[0]-Target[1]+Origin[1]))
    a = Target[0]-simulation(v)[-1].x
    while(a>Error_limit):
        ScanSpeed = max((a/100)**2/100,0.01)
        v = v +ScanSpeed
        a = Target[0]-simulation(v)[-1].x
        print 'v:'+str(v)
    print 'v:'+str(v)
    return v
                

v = scanning()
a = Target[0]-simulation(v)[-1].x
print 'dx:  '+str(a)
b = Drag_cannon(flight_state(Origin[0], Origin[0], v, v,Target[0],Target[1], 0),_dt=0.1)
b.shoot()
b.show_trajectory()
show()
