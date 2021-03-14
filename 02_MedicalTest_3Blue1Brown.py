from bayes import *
from random import random
""" 
##### Bayes Experiment 02 #####
Use the test data from the previous file to simulate the testing history of two patients
"""

def rand_bernoulli( probTrue ):
    """ Return `1` with `probTrue`, Otherwise return 0 with 1 - `probTrue` """
    return ( 1 if ( random() <= probTrue ) else 0 )


def simulate_test( testPower, cancerStatus ):
    """ Simulate test results given both the test predictive power and the actual `cancerStatus` """
    probPos = testPower[ cancerStatus ][1]
    return rand_bernoulli( probPos )


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


def max_dict_key( dct ):
    """ Return the key with the highest numeric value """
    maxVal = float('-inf')
    maxKey = None
    for k, v in dct.items():
        if isnumeric( v ) and (v > maxVal):
            maxVal = v 
            maxKey = k
    return maxKey


def test_patient_until_confident( patient, testPower, stopThresh, initialDist ):
    """ Administer tests with `testPower` to `patient` until the `stopThresh` has been reached """
    
    # 0. Set up the problem
    tstRes   = simulate_test( testPower, patient['cancer'] )
    iterDist = update_odds_with_evidence( initialDist, testPower, tstRes )
    pFor     = get_prob_from_odds( iterDist, 1 )
    pAgn     = get_prob_from_odds( iterDist, 0 )
    i        = 1
    
    def give_result():
        print()
        print( "Odds the Patient has Breast Cancer after test #" , i, ", which came back as" , tstRes )
        pprint( iterDist )
        print( "or equivalently " , iterDist[1] , ':' , iterDist[0] )
        print( "or equivalently " , iterDist[1] , '/' , ( iterDist[1] + iterDist[0] ) , '=' ,
               iterDist[1] / ( iterDist[1] + iterDist[0] ) )
        print()

    # 1. Iterate until we are confident about an answer
    while( max( pFor, pAgn ) < stopThresh ):
        
        give_result()

        tstRes   = simulate_test( testPower, patient['cancer'] )
        iterDist = update_odds_with_evidence( iterDist, testPower, tstRes )
        pFor     = get_prob_from_odds( iterDist, 1 )
        pAgn     = get_prob_from_odds( iterDist, 0 )
        i += 1

    give_result()

    # 2. Print the result
    result = max_dict_key( iterDist )
    rsProb = get_prob_from_odds( iterDist, result )
    print( "After conducting", i, "tests, we have", rsProb, "certainty that the patient status is", result )
    print( "Actual patient cancer status is" , patient['cancer'] )


########## MAIN ###################################################################################

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

patient1 = { 'cancer' : 1 } # `patient1` HAS cancer
patient2 = { 'cancer' : 0 } # `patient2` does NOT have cancer

test_patient_until_confident( patient1, testEfficacy, 0.95, outcomeOdds )
print( "\n#########################################\n" )
test_patient_until_confident( patient2, testEfficacy, 0.9995, outcomeOdds )