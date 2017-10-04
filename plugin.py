import os
from math import *
import time

def results(fields, original_query):
    exp = fields['~expression']
    #print exp
    try:
        time.sleep(0.2) # A buffer time so it doesn't display "No Results"
        ans = eval(exp)
        #print ans
    except Exception as e:
        # print e
        ans = 'N/A'
    return {
        "title": "{0}".format(ans)
        }

def run(expression):
    os.system('echo "{0}"'.format(exp))

def amu(compound):
    import re
    import json

    # Splits compound up based on upper case letters
    path = os.path.dirname(os.path.realpath(__file__))
    tot_mass = 0
    elements_moles = []
    for c in compound:
        if c.isupper():
            elements_moles+=[[c,1]]
        elif c.isdigit():
            elements_moles[len(elements_moles)-1][1] = int(c)
        else:
            elements_moles[len(elements_moles)-1][0] += c

    elements_moles = dict(elements_moles)
    #print elements_moles

    with open(path + '/periodic-data.json') as data_file:
        p_table = json.load(data_file)

    for p_elem in p_table:
        if p_elem['symbol'] in elements_moles.keys():
            num_moles = elements_moles[p_elem['symbol']]
            mass = p_elem['atomicMass']
            parenthesies = mass.find('(')
            if parenthesies != -1:
                mass = float(mass[0:parenthesies])
            else:
                mass = float(mass)
            tot_mass += mass * num_moles
    return tot_mass

def no_nums(s):
    new_str = s
    for c in s:
        if c.isdigit():
            new_str = new_str.replace(c,'')
    return new_str

#print eval('amu(\'Hg\')')
#print amu('SO4')
#inp="amu('Hg')"
#print results({'~expression':inp} , '')
