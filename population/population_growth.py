# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 12:23:45 2016
   Population growth problems
@author: yi cao
"""
import numpy as np
import matplotlib.pyplot as plt

def draw_pic(a,b,N0):
    a = float(a)
    b = float(b)
    N0 = float(N0)
    N=[]
    N.append(N0)
    
    if b == 0:
        final = np.inf
        max_t = 0.4
    else:
        final = a/b
        max_t = np.log(final*9)/a
        
    t = np.linspace(0,max_t,1000)
    #Euler method 数值解
    for i in range(999):
        N_new = N[i]+(a*N[i]-b*N[i]**2)*t[1]
        N.append(N_new)
    #exact solution 解析解
    n = (a*np.exp(a*t))/(a/N0-b+b*np.exp(a*t))          
    #绘图
    plt.figure(figsize=(10,6))
    plt.plot(t,n,label="exact solution",color="red",linewidth=1)
    plt.plot(t,N,label="Euler method",color="green",linewidth=3,linestyle='--')    
    plt.plot([0,1.0],[final,final],label='a/b : '+str(final),color='blue',linewidth=1,linestyle="--")    
    plt.xlabel("Time(t)")
    plt.ylabel("population(n)")
    plt.title("Population growth problems")
    plt.axis([0,max_t,min(N)*0.9,max(N)*1.1])
    plt.legend(loc='best')
    plt.savefig(str(a+b+N0)+'.png')
    plt.show()

print 'when b=0, population growth curve'        
draw_pic(30,0,1000)
print 'when N0=10,a=10,b=3, population growth curve'
draw_pic(10,3,10)
print 'when N0=1000,a=10,b=0.01, population growth curve'
draw_pic(10,0.01,1000)
print 'Now you can draw your curve'
a = raw_input('input a:')
b = raw_input('input b:')
N0 = raw_input('input N0:')
draw_pic(a,b,N0)
