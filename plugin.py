import os
from math import *
import time

def results(fields, original_query):
    exp = fields['~expression']
    exp = format_for_eval(exp)

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
    elements_moles = get_element_mole_form(compound)

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

            # Some masses are presented as 4.0124(4), so this removes the pthesies
            pthesies = mass.find('(')
            if pthesies != -1:
                mass = float(mass[0:pthesies])
            else:
                mass = float(mass)

            tot_mass += mass * num_moles
    return tot_mass

# Creates a dict ex: H2O would be {'H': 2, 'O': 1}
def get_element_mole_form(compound):
    elements_moles = []
    compound = compound.replace('.','')
    i = 0
    while i < len(compound):
        c = compound[i]
        if c.isupper():
            keys = [k for k,v in elements_moles]
            if c not in keys:
                elements_moles += [[c,1]]
            else:
                elements_moles[keys.index(c)][1] += 1

        elif c.isdigit():
            factor = ''
            x = i
            while x < len(compound) and compound[x].isdigit():
                factor += compound[x]
                x += 1
            elements_moles[len(elements_moles)-1][1] += int(factor)-1
            i = x-1

        else:
            elements_moles[len(elements_moles)-1][0] += c
        i += 1

    return dict(elements_moles)

# TODO: Clean up this garbage, smh
# Performs various parsing to optimize the input for the eval() function
def format_for_eval(exp):

    #TODO: Clean this up and move over to get_element_mole_form()
    # Distributes moles for parentheses
    i = 0
    while i < len(exp):
        i = exp.find('amu(', i)
        if i == -1:
            break
        i += len('amu(') + 1
        open_p_indx = []
        close_p_indx = []
        for j in range(i, len(exp)):
            if exp[j] == '(':
                open_p_indx += [j]
            elif exp[j] == ')':
                if len(open_p_indx) == len(close_p_indx):
                    i = j
                    break
                else:
                    close_p_indx += [j]

        for k in range(len(open_p_indx)):
            inner_cmpnd = exp[open_p_indx[k]+1:close_p_indx[k]].replace(' ','')
            next_char = exp[close_p_indx[k]+1]
            if next_char.isdigit():
                x = close_p_indx[k]+2
                factor = ''
                while x < len(exp) and next_char.isdigit():
                    factor += next_char
                    next_char = exp[x]
                    x += 1
                elem_mol = get_element_mole_form(inner_cmpnd)
                for e in elem_mol.keys():
                    elem_mol[e] *= int(factor)
                inner_cmpnd_distr = ''.join([k + str(v) for k,v in elem_mol.iteritems()])
                replace_target = '(' + inner_cmpnd + ')' + factor
                exp = exp.replace(replace_target, inner_cmpnd_distr)
            else:
                replace_target = '(' + inner_cmpnd + ')'
                exp = exp.replace(replace_target, inner_cmpnd)

    # Adds quotes around custom functions
    custom_funcs = ['amu']
    for func in custom_funcs:
        i = 0
        while i < len(exp):
            i = exp.find(func, i)
            if i == -1:
                break
            i += len(func)+1
            exp = insert(exp, i, '\'')
            counts = {'(': 0, ')': 0}

            exp = insert(exp, exp.find(')', i), '\'')

    #TODO: Fix - breaks numbers that already have a decimal
    # Turns ints into floats
    i = 0
    while i < len(exp)-1:
        if exp[i].isdigit():
            if exp[i+1] == '.':
                # Set to the index of the character after the decimal point
                i += 2
                # Skip past the decimal places eg: '123.312.' doesn't occur
                while i < len(exp)-1 and exp[i].isdigit():
                    i+=1
            elif not exp[i+1].isdigit():
                exp = insert(exp, i+1, '.')
        i += 1

    return exp

# Inserts a string at position i of input_string
def insert(input_string, i, ins):
    return input_string[:i] + str(ins) + input_string[i:]

#print eval('amu(\'Hg\')'])
#print amu('SO4.')
#print format_for_eval('23.123/amu(S(OH)3)')
#inp='amu(Pb(SO4)2)/amu(H)'
#print results({'~expression':inp} , '')
