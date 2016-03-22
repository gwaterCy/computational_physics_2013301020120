

#第四次作业
##摘要  
人口增长问题(Population growth problems)
用Euler Method 求出了1.6题的近似解，并和其Exact Solution 比较

-----
##背景介绍  
人口增长模型公式：
![equation](https://raw.githubusercontent.com/whuCanon/computationalphysics_N2013301020085/master/chapter1/Resource/formula1.png)
该等式描述了人口数量随时间变化的规律，aN项为新出生人口，-bN<sup>2</sup>代表死亡数量。b=0时，人口呈指数上涨
##正文

###实现原理  

#### Euler方法的一阶近似解
![equation](https://raw.githubusercontent.com/whuCanon/computationalphysics_N2013301020085/master/chapter1/Resource/formula2.png)  
程序实现：
 
    N.append(N0)
    t = np.linspace(0,max_t,1000)
    for i in range(999):
        N_new = N[i]+(a*N[i]-b*N[i]**2)*t[1]
        N.append(N_new)
        
#### 直接求得的解析解 (Exact Solution)
![](http://i.imgur.com/OABFxtC.png)
程序实现：

    t = np.linspace(0,max_t,1000)
    n = (a*np.exp(a*t))/(a/N0-b+b*np.exp(a*t)) 

###程序源码
	
[查看源码](https://github.com/breakingDboy/computational_physics_2013301020120/blob/master/population/population_growth)
	
###结果分析  
当b = 0时，N 呈指数增长。红色线为解析解，绿色虚线为近似解
![b=0](http://i.imgur.com/OG7UlaD.png)		
当a = 10,b = 3 ,N0 = 10. 人口增长曲线如下：
![](http://i.imgur.com/J4ErPHg.png)		
当a=100,b=0.1,N0 = 1000 时，人口曲线是一天稳定的直线：
![](http://i.imgur.com/l9LorWT.png)				
																																																																																			

##结论  
当b=0时，即人没有死亡时，人口数量呈指数增长。
当b != 0 是 ，人口总数总是趋向于a/b 


##致谢
>-该md文档，借鉴刘文焘同学的报告格式！（感谢）

------
> Written with [StackEdit](https://stackedit.io/).