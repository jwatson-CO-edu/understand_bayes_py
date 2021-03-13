from pprint import pprint
""" 
##### Bayes Experiment 01 #####
The medical test paradox: Can redesigning Bayes rule help? by 3Blue1Brown
https://www.youtube.com/watch?v=lG4VkPoG3ko

Step 1: Express the prior with odds
Step 2: Compute Bayes Factor
Step 3: Multiply
"""

from bayes import *

outcomeOdds = {
    1 :  1 ,
    0 : 99 ,
}

testEfficacy = {
    1 : {
        1 :  9/ 10 , # True  Positives
        0 : 89/990 , # False Positives
    },
    0 : {
        1 : 1 -  9/ 10 , # False Negatives = 1 - True  Positives
        0 : 1 - 89/990 , # True  Negatives = 1 - False Positives
    },
}

print()
print( "Original Odds a Woman has Breast Cancer" )
pprint( outcomeOdds )
print()

def update_odds_with_evidence( prevalence, testPower, evdnc ):
    """ Compute a new odds of an outcome """
    evPos = evdnc
    evNeg = 1 - evdnc
    oddsPos = prevalence[evPos]/prevalence[evNeg] * testPower[evdnc][evPos]/testPower[evdnc][evNeg]
    oddsNeg = float('nan')
    if oddsPos > 1:
        oddsNeg = 1.0
    elif oddsPos > 0:
        oddsNeg = 1 / oddsPos
        oddsPos = 1.0
    return {
        evPos : oddsPos ,
        evNeg : oddsNeg ,
    }
    
iterDist = outcomeOdds
N        = 5
testRes  = 1

for i in range( N ):
    iterDist = update_odds_with_evidence( iterDist, testEfficacy, 1 )
    print()
    print( "Odds a Woman has Breast Cancer after" , i+1, "test results of" , testRes )
    pprint( iterDist )
    print( "or equivalently " , iterDist[1] , ':' , iterDist[0] )
    print( "or equivalently " , iterDist[1] , '/' , ( iterDist[1] + iterDist[0] ) )
    print()
