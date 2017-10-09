import os
from math import *
import time

def results(fields, original_query):
    exp = fields['~expression']
    exp = format_for_eval(exp)

    try:
        # A buffer time to try to fix "No results." bug
        time.sleep(0.2)

        ans = eval(exp)
    except Exception as e:
        ans = 'N/A'
    return {
        "title": "{0}".format(ans)
        }

def run(expression):
    os.system('echo "{0}"'.format(exp))

def amu(compound):
    import json
    tot_mass = 0

    # A dict of each element and their respective # of moles
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

            # Some masses are presented as 4.0124(4), so this removes the parentheses
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

# TODO: Clean up and comment this garbage, smh
# Performs various parsing to optimize the input for the eval() function
def format_for_eval(exp):

    #TODO: Clean this up and move over to get_element_mole_form()
    # Distributes moles for parentheses
    i = 0
    while i < len(exp):
        i = exp.find('amu(', i)
        if i == -1:
            break

        i += len('amu(')
        open_p_indx = []
        close_p_indx = []

        # Gets all of the indexes of the inner parentheses in the amu function
        for j in range(i, len(exp)):
            if exp[j] == '(':
                open_p_indx += [j]
            elif exp[j] == ')':
                # If there are are more closed parentheses then open ones
                if len(open_p_indx) == len(close_p_indx):
                    i = j
                    break
                else:
                    close_p_indx += [j]

        # Goes through all of the open_p, closed_p pairs
        for k in range(len(open_p_indx)):
            # The compound surrounded in parentheses eg. in Cu(SO4)3,
            # inner_cmpnd = 'SO4'
            inner_cmpnd = exp[open_p_indx[k]+1:close_p_indx[k]].replace(' ','')

            # The char after the particular closed parentheses so in '(OH)3',
            # next_char = '3'
            next_char = exp[close_p_indx[k]+1]

            # If a digit follows the parentheses
            if next_char.isdigit():

                # The number that is being distributed into inner_cmpnd
                factor = ''

                x = close_p_indx[k]+2
                while x < len(exp) and next_char.isdigit():
                    factor += next_char
                    next_char = exp[x]
                    x += 1

                elem_mol = get_element_mole_form(inner_cmpnd)

                # Distrubutes the factor to the moles of the inner_cmpnd
                for e in elem_mol.keys():
                    elem_mol[e] *= int(factor)

                # Forms the distributed inner_cmpnd back into a string from the
                # elem_mol dict it was turned into
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
            exp = insert(exp, exp.find(')', i), '\'')

    # Turns ints into floats
    i = 0
    while i < len(exp)-1:
        if exp[i].isdigit():
            if exp[i+1] == '.':
                # Sets index to character after the decimal point
                i += 2

                # Skips past the decimal places so '123.312.' doesn't occur
                while i < len(exp)-1 and exp[i].isdigit():
                    i+=1
            elif not exp[i+1].isdigit():
                exp = insert(exp, i+1, '.')

        # If the number starts with a decimal eg .123
        elif exp[i] == '.':
            i += 2
            while i < len(exp)-1 and exp[i].isdigit():
                i+=1
        i += 1

    return exp

# Inserts a string at position i of input_string
def insert(input_string, i, ins):
    return input_string[:i] + str(ins) + input_string[i:]

print format_for_eval('amu(Cu(SK4)3)')
#inp='amu(Pb(SO4)2)/amu(H)'
#print results({'~expression':inp} , '')
