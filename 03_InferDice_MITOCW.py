from pprint import pprint
from random import randrange, choice
from bayes import normalize_dist, max_dict_key_val
""" 
##### Bayes Experiment 03 #####
Update beliefs on more than 2 classes
"""

dieTypes = [4, 6, 8, 12, 20]

class Die:
    """ A fair die """
    def __init__( self, sides ):
        """ Set the number of sides """
        self.sides = sides
    def __str__( self ):
        """ Represent die with D&D nomenclature """
        return "d"+str(self.sides)
    def roll( self ):
        """ Return the result of one die roll """
        return randrange( 1, self.sides+1 )
    def prob_evidence( self, evidence ):
        """ What is the probability of seeing the evidence on this die? """
        if 0 < evidence <= self.sides:
            return 1.0 / self.sides
        else:
            return 0.0

d6 = Die(6)
for i in range(3):
    print( d6, ':', d6.roll() )

cup = [ Die(s) for s in dieTypes ] # Create a cup with one of each kind of die

# Calc the probability of drawing a die of any specific type
priors = {}
for d in cup:
    s = d.sides
    if s in priors:
        priors[s] += 1
    else:
        priors[s]  = 1

priors = normalize_dist( priors )
pprint( priors )

def prob_outcome_per_type( outcome ):
    """ Build a table of the likelihood of this outcome on each type of die """
    conditionalP = {}
    for t in dieTypes:
        conditionalP[t] = Die(t).prob_evidence( outcome )
    return conditionalP


def roll_and_update( die, priors_ ):
    """ Roll the die and report how it changes our posterior probs. """
    roll_i    = die.roll()
    cProbRoll = prob_outcome_per_type( roll_i )
    posterior = {}
    for dn in cProbRoll:
        posterior[dn] = priors_[dn] * cProbRoll[dn]
    posterior = normalize_dist( posterior )
    print( "The updated posterior beliefs after rolling a", roll_i, "are:" )
    pprint( posterior )
    return posterior

########## MAIN ###################################################################################

# 1. Pick a die from the cup
cDie = choice( cup )

# 2. Roll once and gather some evidence
iterDist = roll_and_update( cDie, priors )
mk, mv   = max_dict_key_val( iterDist )
i        = 1
thresh   = 0.995

# 3. Roll the die again and again until we are sure of what we have
while( mv < thresh ):
    i += 1
    print( "### Iteration" , i , "###" )
    iterDist = roll_and_update( cDie, iterDist )
    mk, mv   = max_dict_key_val( iterDist )
    print()

# 4. Check the results
print( "\nPredicted: ____ d" + str(mk) )
print( "The answer was:", cDie )