# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 19:39:43 2023

@author: bensh
"""

import random
from copy import deepcopy

def is_valid_expression(expression_object, function_symbols, leaf_symbols):
    """
    A python function that returns true if the given object
    is in the correct form of an expression. An object is an expression
    if it is an integer, a specific leaf symbol, or a list containing
    a pre-order expression
    
    Parameters
    ----------
    expression_object : any
        an object to be tested
    function_symbols : list
        list of binary operations
    leaf_symbols : list
        list of symbols that can be leaves
        
    Returns
    -------
    boolean
    """
    
    if type(expression_object) == list:
        if len(expression_object) == 3:
            return expression_object[0] in function_symbols\
                and is_valid_expression(expression_object[1], function_symbols, leaf_symbols)\
                and is_valid_expression(expression_object[2], function_symbols, leaf_symbols)
    elif type(expression_object) == int:
        return True
    elif type(expression_object) == str:
        return True if object in leaf_symbols else False
    return False

def depth(expression):
    """

    Parameters
    ----------
    expression : List
        a pre-order expression tree in list form

    Returns
    -------
    The maximum depth of the tree : int

    """
    
    if type(expression) == list:
        return 1 + max(depth(expression[1]), depth(expression[2]))
    else:
        return 0
    
def evaluate(expression, bindings):
    """

    Parameters
    ----------
    expression : List
        a pre-order expression tree in list form
    bindings : Dict
        A dictionary where the keys are strings
        In the case of an operation, the values are binary functions.
        In the case of a variable, the values are integers

    Returns
    -------
    An integer value of the expression
    """
    
    if type(expression) == list:
        return bindings[expression[0]](evaluate(expression[1], bindings),\
                                       evaluate(expression[2], bindings))
    elif type(expression) == str:
        return bindings[expression]
    else:
        return expression
    
def random_expression(function_symbols,leaves, max_depth, current_depth=0):
    """
    Parameters
    ----------
    function_symbols : SET
        set of operators a function can use
    leaves : set
        set of leaves of the expression
    max_depth : int
        max depth of the tree

    Returns
    -------
    List of expression

    """
    
    if random.random() <= 0.7 or current_depth >= max_depth:
        return leaves[random.randint(0, len(leaves)-1)]
    else:
        return [function_symbols[random.randint(0, len(function_symbols)-1)],\
                random_expression(function_symbols, leaves, max_depth, current_depth+1),\
                random_expression(function_symbols, leaves, max_depth, current_depth+1)]

def generate_rest(initial_sequence, expression, length):
    """
    takes a sequence and uses an expression to generate the next length
    terms of the sequence

    Parameters
    ----------
    initial_sequence : List
        inital sequence to be extended
    expression : List
        a function of x, y, and i
    length : int
        Dthe number of terms to be expanded upon

    Returns
    -------
    List of next items
    """
    next_items = []
    while len(next_items) < length:
        current_sequence = initial_sequence + next_items
        i = len(current_sequence)
        bindings = {"x": current_sequence[i-2], "y": current_sequence[i-1], "i": i,
                    "*": lambda a, b: a*b, "-": lambda a, b: a-b, "+": lambda a, b: a+b}
        item_to_add = evaluate(expression, bindings)
        next_items.append(item_to_add)
    return next_items

def get_fitness(sequence, expression):
    """

    Parameters
    ----------
    sequence : List
        an integer sequence of at least 5
    expression : List
        a list representation of a function

    Returns
    -------
    A measure of the algorithms fitness,
    obtained by performing mean squares difference on the elements
    of the list after the first 2 elements

    """
    input_sequence = sequence[:2]
    test_sequence = sequence[2:]
    
    prediction = generate_rest(input_sequence, expression, len(test_sequence))
    score = 0
    for index in range(len(test_sequence)):
        score += (test_sequence[index] - prediction[index]) ** 2
        
    try:
        score = score / len(test_sequence)
    except OverflowError:
        score = float('inf')
    return score

def get_fitness_number_correct(sequence, expression):
    """

    Parameters
    ----------
    sequence : list
        sequence of terms
    expression : list
        pre-order expression in list form

    Returns
    -------
    integer score

    """
    input_sequence = sequence[:2]
    test_sequence = sequence[2:]
    
    prediction = generate_rest(input_sequence, expression, len(test_sequence))
    score = 0
    for index in range(len(test_sequence)):
        if test_sequence[index] == prediction[index]:
            score +=1
    return score
    
    
    
def roulette_wheel_selection(population, fitness, number_iterations):
    """
    performs a roulette wheel selection by examining the fitness of each indevidual in the population,
    and assigning each one an adiquit portion of the wheel. Then performs number_iterations selections. 

    Parameters
    ----------
    population : List
        list of individuals in the population
    fitness : list
        entries in list are fitness of the individual in population.
    number_iterations : int
        number of entries to be selected

    Returns
    -------
    List of selected individuals

    """
    wheel = []
    total_fitness = 0
    for i in range(len(population)):
        total_fitness += fitness[i]
        wheel.append(total_fitness)
        
    selection = []
    for i in range(number_iterations):
        spin_score = random.random() * total_fitness
        index = 0
        while wheel[index] < spin_score:
            index += 1
        selection.append(population[index-1])
    
    return selection

def tournament_selection(population, fitness, size, number_iterations):
    """
    performs tournament selection on a randomly allocated section of the population,
    choosing the fittest individual each iteration.
      
    Parameters
    ----------
    population: List
        list of individuals in the population
    fitness : list
        fitnesses of each individual in the population
    size: int
        number of individuals in each tornament
    number_iterations: int
        the number of times the selection is to be run
    
    Returns
    -------
    List of selected individuals
    
      """
    result = []
    for round in range(number_iterations):  
        selection = []
        for i in range(size):
            index = random.randint(0, len(population) - 1)
            selection += [(population[index], fitness[index])]
            
        best_tuple = min(selection, key = lambda s: s[1])
        result.append(best_tuple[0])
        
    return result
    
    

def reproduce(parent_a, parent_b, max_depth):
    """
    Takes two individuals in the population and randomly swaps subtrees

    Parameters
    ----------
    exp_a : List
        a pre-order expression in list form
    exp_b : List
        a pre-order expression in list form
    max_depth: int
        the max depth of subtrees to swap
        
    Returns
    -------
    two pre-order expressions in list form

    """
    if type(parent_a) == list and type(parent_b) == list:
        exp_a = deepcopy(parent_a)
        exp_b = deepcopy(parent_b)
        num_crossovers = random.randint(1, 3)
        while num_crossovers > 0:
            num_crossovers -= 1
            subtree_a, path_a = get_random_subtree(exp_a)
            subtree_b, path_b = get_random_subtree(exp_b)
            while len(path_a) + depth(subtree_b) > max_depth and\
                len(path_b) + depth(subtree_a) > max_depth:
                subtree_a, path_a = get_random_subtree(exp_a)
                subtree_b, path_b = get_random_subtree(exp_b)    
            
            if len(path_a) != 0 and len(path_b) != 0:
                new_child_a = deepcopy(exp_a)
                new_child_b = deepcopy(exp_b)
                
                tree_replace(new_child_a, path_a, subtree_b)
                tree_replace(new_child_b, path_b, subtree_a)
                
                exp_a = new_child_a
                exp_b = new_child_b
            
        return exp_a, exp_b
    else:
        return parent_a, parent_b
        
        
        
def tree_replace(expression, path, subtree):
    """replaces the subtree on the given path with the given subtree
    
    Parameters
    ----------
    expression: List
        An expression in preorder form
    path: list
        The path the subtree to replace lies on
    subtree: List
        An expression to be swapped out

    Returns
    -------
    None
    """
    if len(path) > 0:
        current_exp=expression
        for depth in range(len(path)-1):
            current_exp = current_exp[path[depth]]
        current_exp[path[-1]] = subtree
    else:
        raise ValueError("length of path must be at least 1")
    
    
def get_random_subtree(expression, decision=[]):
    """returns a random subtree of an expression, along with its location
    
    Parameters
    ----------
    expression: List
        a preorder expression in list form
    decision: List
        the current path that has been traversed
        
    Returns
    -------
    The path that has been traversed
    """
    movement = random.randint(0, 2)
    if type(expression[movement]) == list:
        return get_random_subtree(expression[movement], decision + [movement])
    return (expression, decision) if movement == 0 else (expression[movement], decision + [movement])

def mutate(expression,function_symbols, leaves, max_depth):
    """chooses a random subtree on an expression and replaces it with a new one"""
    exp = deepcopy(expression)
    if type(exp) == list:
        subtree, path = get_random_subtree(exp)
        mutation = random_expression(function_symbols, leaves, max_depth-len(path))
        if len(path) > 0:
            tree_replace(exp, path, mutation)
            return exp
        else:
            return mutation
    else:
        return random_expression(function_symbols, leaves, max_depth)
    

def predict_rest(sequence):
    """
    uses an evolutionary algorithm, predicts the next five items
    following the inputted sequence

    Parameters
    ----------
    sequence : List
        A five item sequence of integers

    Returns
    -------
    The predicted next five items in the sequence
    """
    
    INTEGER_RANGE = list(range(-2, 3))
    VARIABLE_NAMES = ['x', 'y', 'i']
    LEAVES = INTEGER_RANGE + VARIABLE_NAMES
    FUNCTION_SYMBOLS = ["+", "-", "*"]
    
    MAX_DEPTH = 4
    
    POPULATION_SIZE = 300
    population = [random_expression(FUNCTION_SYMBOLS, LEAVES, MAX_DEPTH) for i in range(POPULATION_SIZE)]
    
    
    number_iterations = 0
    MAX_ITERATIONS = 500
    fittest_sequence = population[0]
    while get_fitness(sequence, fittest_sequence) > 0 and number_iterations < MAX_ITERATIONS:
        number_iterations += 1
        
        # First evaluate the fitness of the cycle
        fitness = [get_fitness_number_correct(sequence, expression) for expression in population]
        
        fittest_sequence_index = max(list(range(len(population))), key=lambda i: fitness[i])
        fittest_sequence = population[fittest_sequence_index]
        
        # Then choose a percentage to survive
        percent_direct_survivors = 0.7
        survivors = tournament_selection(population, fitness,\
                    4, int(POPULATION_SIZE // (1/percent_direct_survivors)))
        
        # breed survivors until numbers are back at peak
        bred_survivors = deepcopy(survivors)
        bred_survivors.append(fittest_sequence)
        while len(bred_survivors) < POPULATION_SIZE:
            index_1 = random.randint(0, len(survivors)-1)
            index_2 = random.randint(0, len(survivors)-1)
            
            child_1, child_2 = reproduce(survivors[index_1], survivors[index_2], MAX_DEPTH)
            bred_survivors += [child_1, child_2]
        
        #finally, mutations
        for index in range(len(bred_survivors)):
            if random.random() < 0.2:
                bred_survivors[index] = mutate(bred_survivors[index], FUNCTION_SYMBOLS, LEAVES, MAX_DEPTH)
        population = bred_survivors
        
    return generate_rest(sequence, fittest_sequence, 5), format_expression(fittest_sequence)

def format_expression(expression):
    """takes in an expression, and then puts it in a nice form for output
    
    Parameters
    ----------
    expression: List
        a preorder representation of an expression in list form
    
    Returns
    -------
    the expression in string form"""
    if type(expression) == list:
        return f"({format_expression(expression[1])} {expression[0]}  {format_expression(expression[2])})"
    else:
        return str(expression)
        

def get_correct_percentage(sequence, expected_result, num_iterations=100):
    """ runs predict rest a set number of iterations, and prints the percentage that
    give the correct results

    Parameters
    ----------
    sequence: List
        an integer sequence
    expected_result: List
        The next 5 outputs of the sequence
    num_iterations: int
        number of times the simulation is to be run
    
    Returns
    -------
    None
    """
    score = 0
    for i in range(num_iterations):
        print(i)
        if predict_rest(sequence) == expected_result:
            score += 1
    print(f"{score/num_iterations} percent correct")
    
def test_cases():
    """
    A selection of test cases to be run
    """
    
    sequences = [[0, 1, 2, 3, 4, 5, 6, 7],
                [0, 2, 4, 6, 8, 10, 12, 14],
                [31, 29, 27, 25, 23, 21],
                [0, 1, 4, 9, 16, 25, 36, 49],
                [3, 2, 3, 6, 11, 18, 27, 38],
                [0, 1, 1, 2, 3, 5, 8, 13],
                [0, -1, 1, 0, 1, -1, 2, -1],
                [1, 3, -5, 13, -31, 75, -181, 437]
                 ]
    for sequence in sequences:
        print(f"Sequence: {sequence}, predicted output: {predict_rest(sequence)[0]}")    
def main():
    """
    main function. Called when run
    """

    test_cases()
        
if __name__ == "__main__":
    main()