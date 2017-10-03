import os
from math import *

def results(fields, original_query):
    exp = fields['~expression']
    #print exp
    try:
        ans = eval(exp)
        #print ans
    except Exception as e:
        #print e
        ans = 'N/A'
    return {
        "title": "{0}".format(ans),
        "run_args": [exp]
    }

def run(expression):
    os.system('echo "{0}"'.format(exp))

def amu(element):
    import json
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/periodic-data.json') as data_file:
        p_table = json.load(data_file)
    for elem in p_table:
        if elem['symbol'] == element:
            mass = elem['atomicMass']
            parenthesies = mass.find('(')
            if parenthesies != -1:
                return float(mass[0:parenthesies])
            return float(mass)

#print eval('amu(\'Hg\')')
#print amu('Li')
#inp="amu('Hg')"
#print results({'~expression':inp} , '')
