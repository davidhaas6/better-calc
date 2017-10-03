import os
from math import *
import time

def results(fields, original_query):
    exp = fields['~expression']
    #print exp
    try:
        time.sleep(0.1) # A buffer time so it doesn't display "No Results"
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
    split_atoms = re.findall(r'[A-Z]+[^A-Z]*', compound)
    elements = [no_nums(e) for e in split_atoms]
    moles = []
    for e in split_atoms:
        num = re.findall('\d', e)
        print num
        if not num:
            moles+=[1]
        else:
            moles+=[int(''.join(num))]

    elements_with_moles = dict()
    for i in range(len(elements)):
        elements_with_moles[elements[i]] = moles[i]
    # print split_atoms, elements_with_moles

    with open(path + '/periodic-data.json') as data_file:
        p_table = json.load(data_file)

    for p_elem in p_table:
        if p_elem['symbol'] in elements_with_moles.keys():
            num_moles = elements_with_moles[p_elem['symbol']]
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
# print amu('C4H10')
#inp="amu('Hg')"
#print results({'~expression':inp} , '')
