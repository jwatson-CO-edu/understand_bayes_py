from pprint import pprint

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