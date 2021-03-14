########## INIT ###################################################################################

from pprint import pprint
from random import random

########## UTILITIES ##############################################################################


def rand_bernoulli( probTrue ):
    """ Return `1` with `probTrue`, Otherwise return 0 with 1 - `probTrue` """
    return ( 1 if ( random() <= probTrue ) else 0 )


def isnumeric( numStr ):
    """ Hack to determine if a non-unicode string is numeric or not """
    numStr = str( numStr )
    try:
        int( numStr )
        return True
    except:
        try:
            float( numStr )
            return True
        except:
            return False


def max_dict_key_val( dct ):
    """ Return the key with the highest numeric value """
    maxVal = float('-inf')
    maxKey = None
    for k, v in dct.items():
        if isnumeric( v ) and (v > maxVal):
            maxVal = v 
            maxKey = k
    return maxKey, maxVal



########## STATISTICS #############################################################################

def total_pop( odds ):
    """ Sum over all categories in the prior odds """
    total = 0
    for k in odds:
        total += odds[k]
    return total


def normalize_dist( odds_ ):
    """ Normalize the distribution so that the sum equals 1.0 """
    total  = total_pop( odds_ )
    rtnDst = dict()
    for k in odds_:
        rtnDst[k] = odds_[k] / total
    return rtnDst


def joint_distribution( outcomeOdds_ , attrDist_ ):
    """ Return the likelihood that the outcome is true given the evidence """
    # 0. Get the prior distribution
    priorDist = normalize_dist( outcomeOdds_ )
    print( "Prior Distribution" ) 
    pprint( priorDist )    
    # 1. Get the joint distribution
    joint = dict()
    for k in priorDist:
        joint[k] = dict()
        for evidence in attrDist_:
            joint[k][evidence] = dict()
            joint[k][evidence][1] = priorDist[k] * attrDist_[ evidence ][ k ]
            joint[k][evidence][0] = priorDist[k] * ( 1 - attrDist_[ evidence ][ k ] )
    return joint


########## BAYES HELPERS ##########################################################################

def prob_outcome_given_evidence( outcomeOdds_ , attrDist_, outcome, trueFals, evidence ):
    """ What is the probability that `outcome` is `trueFals`, given the `evidence` ? """
    
    # 0. Compute the joint distribution
    jointDist = joint_distribution( outcomeOdds_ , attrDist_ )
    print( "Joint Distribution" ) 
    pprint( jointDist )

    # 1. Marginalize 
    normDist = dict()
    for k in outcomeOdds_:
        normDist[k] = jointDist[ k ][ evidence ][ trueFals ]
    normDist = normalize_dist( normDist )

    # N. Fetch prob
    return normDist[ outcome ]


def update_odds_with_evidence( prevalence, testPower, evdnc ):
    """ Compute a new odds of an outcome """
    evPos   = evdnc
    evNeg   = 1 - evdnc
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


def get_prob_from_odds( odds, outcome ):
    """ Get the probability of `outcome` given the `odds` """
    oddFor = odds[ outcome   ]
    oddAgn = odds[ 1-outcome ]
    return oddFor / (oddFor + oddAgn)