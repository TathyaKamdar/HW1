#Problem 3(a)
#100 replications

import random
import math
import statistics
import numpy as np

def Timer():
    global Clock
    global NextFailure
    global NextRepair
    
    if NextFailure < NextRepair:
        result = "Failure"
        Clock = NextFailure
        NextFailure = Infinity
    else:
        result = "Repair"
        Clock = NextRepair
        NextRepair = Infinity
    
    return result

def Failure():
    global S
    global Slast
    global Tlast
    global Area
    global NextFailure
    global NextRepair
    global Clock
    
    S = S - 1
    
    if S == 2:
        NextFailure = Clock + math.ceil(6*random.random())
        NextRepair = Clock + 3.5
    
    elif S == 1:
        NextFailure = Clock + math.ceil(6*random.random())
        NextRepair = NextRepair
    
    Area = Area + Slast * (Clock - Tlast)
    Tlast = Clock
    Slast = S

def Repair():
    global S
    global Slast
    global Tlast
    global Area
    global NextFailure
    global NextRepair
    global Clock
    
    S = S + 1
    
    if S == 2:
        NextRepair = Clock + 3.5
        
    if S == 3:
        NextFailure = NextFailure
        NextRepair = Infinity
    
    Area = Area + Slast * (Clock - Tlast)
    Tlast = Clock
    Slast = S

Infinity = 1000000
random.random()
SumS = 0
SumY = 0
Y = []
Sbar = []

for reps in range(0,100,1):
    NextFailure = math.ceil(6*random.random())
    NextRepair = Infinity
    
    S = 3.0
    Slast = 3.0
    Clock = 0.0
    Tlast = 0.0
    Area = 0.0
    
    while S > 0:
        NextEvent = Timer()
        if NextEvent == "Failure":
            Failure()
        else:
            Repair()
    
  
    SumS = SumS + Area/Clock
    SumY = SumY + Clock
    Y.append(Clock)
    Sbar.append(Area/Clock)

print("Average failure at time " + str(SumY/100) +
      " with average # of functional components " + str(SumS/100))

Y_bar = statistics.mean(Y)
S_bar = statistics.mean(Sbar)

CI_Ybar = [Y_bar - 1.96*np.std(Y)/math.sqrt(100),
           Y_bar + 1.96*np.std(Y)/math.sqrt(100)]
CI_Sbar = [S_bar - 1.96*np.std(Sbar)/math.sqrt(100),
           S_bar + 1.96*np.std(Sbar)/math.sqrt(100)]

print(f"Y_bar: {Y_bar:.4f}, 95% CI: [{CI_Ybar[0]:.4f}, {CI_Ybar[1]:.4f}]")
print(f"S_bar: {S_bar:.4f}, 95% CI: [{CI_Sbar[0]:.4f}, {CI_Sbar[1]:.4f}]")