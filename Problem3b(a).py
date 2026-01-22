import random
import math
import statistics
import numpy as np

def Timer():
    global Clock, NextFailure, NextRepair
    
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
    global S, Slast, Tlast, Area, NextFailure, NextRepair, Clock, TimeAtZero
    
    Area = Area + Slast * (Clock - Tlast)
    
    if Slast == 0:
        TimeAtZero = TimeAtZero + (Clock - Tlast)
    
    Tlast = Clock
    S = S - 1
    Slast = S
    
    if S == 2:
        NextFailure = Clock + math.ceil(6 * random.random())
        NextRepair = Clock + 3.5
    elif S == 1:
        NextFailure = Clock + math.ceil(6 * random.random())
    elif S == 0:
        NextFailure = Infinity

def Repair():
    global S, Slast, Tlast, Area, NextFailure, NextRepair, Clock, TimeAtZero
    
    Area = Area + Slast * (Clock - Tlast)
    
    if Slast == 0:
        TimeAtZero = TimeAtZero + (Clock - Tlast)
    
    Tlast = Clock
    S = S + 1
    Slast = S
    
    if S == 1:
        NextFailure = Clock + math.ceil(6 * random.random())
    elif S == 2:
        NextRepair = Clock + 3.5
    elif S == 3:
        NextRepair = Infinity

Infinity = 1000000
random.seed(1234)

AvgFunctional = []
ProportionFailure = []

for reps in range(0, 100, 1):
    NextFailure = math.ceil(6 * random.random())
    NextRepair = Infinity
    
    S = 3.0
    Slast = 3.0
    Clock = 0.0
    Tlast = 0.0
    Area = 0.0
    TimeAtZero = 0.0
    
    while Clock < 1000:
        NextEvent = Timer()
        
        if Clock >= 1000:
            Area = Area + Slast * (1000 - Tlast)
            if Slast == 0:
                TimeAtZero = TimeAtZero + (1000 - Tlast)
            break
        
        if NextEvent == "Failure":
            Failure()
        else:
            Repair()
    
    AvgS = Area / 1000
    ProportionFail = TimeAtZero / 1000
    
    AvgFunctional.append(AvgS)
    ProportionFailure.append(ProportionFail)

AvgS_mean = statistics.mean(AvgFunctional)
AvgS_std = np.std(AvgFunctional)
CI_AvgS = [AvgS_mean - 1.96 * AvgS_std / math.sqrt(100),
           AvgS_mean + 1.96 * AvgS_std / math.sqrt(100)]

ProportionFail_mean = statistics.mean(ProportionFailure)
ProportionFail_std = np.std(ProportionFailure)
CI_ProportionFail = [ProportionFail_mean - 1.96 * ProportionFail_std / math.sqrt(100),
               ProportionFail_mean + 1.96 * ProportionFail_std / math.sqrt(100)]

print("Proportion of system failure time:", round(ProportionFail_mean, 4))
print("95% CI:", round(CI_ProportionFail[0], 4), "to", round(CI_ProportionFail[1], 4))
print("Average number of functional components:", round(AvgS_mean, 4))
print("95% CI:", round(CI_AvgS[0], 4), "to", round(CI_AvgS[1], 4))
