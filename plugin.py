import os
from math import *
import time

def results(fields, original_query):
    exp = fields['~expression']
    exp = format_for_eval(exp)
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
    import json
    tot_mass = 0
    elements_moles = []

    # Creates a dict ex: H2O would be{'H': 2, 'O': 1}
    for c in compound:
        if c.isupper():
            elements_moles += [[c,1]]
        elif c.isdigit():
            elements_moles[len(elements_moles)-1][1] = int(c)
        else:
            elements_moles[len(elements_moles)-1][0] += c

    elements_moles = dict(elements_moles)
    #print elements_moles

    # Gets path of folder containing file
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/periodic-data.json') as data_file:
        p_table = json.load(data_file)

    # Goes through each element in the periodic table
    for p_elem in p_table:

        # Checks if the current element is in the compound
        if p_elem['symbol'] in elements_moles.keys():
            num_moles = elements_moles[p_elem['symbol']]
            mass = p_elem['atomicMass']

            # Some masses are presented as 4.0124(4), so this removes the parenthesies
            parenthesies = mass.find('(')
            if parenthesies != -1:
                mass = float(mass[0:parenthesies])
            else:
                mass = float(mass)

            tot_mass += mass * num_moles
    return tot_mass

# Adds quotes around inputs for custom functions, turns ints into floats
def format_for_eval(exp):
    # Adds quotes
    custom_funcs = ['amu']
    for func in custom_funcs:
        index = 0
        while index < len(exp):
            index = exp.find(func, index)
            if index == -1:
                break
            index += len(func)+1
            exp = insert(exp, index, '\'')
            exp = insert(exp, exp.find(')', index), '\'')

    # Turns ints into floats
    i = 0
    while i < len(exp)-1:
        if exp[i].isdigit() and not exp[i+1].isdigit():
            exp = insert(exp, i+1, '.')
            i += 1
        i += 1
    if exp[i].isdigit():
        exp = insert(exp, i+1, '.')

    return exp


# Inserts a string at position index of input_string
def insert(input_string, index, ins):
    return input_string[:index] + str(ins) + input_string[index:]

#print eval('amu(\'Hg\')')
#print amu('SO4')
#inp="1/1"
#print results({'~expression':inp} , '')
