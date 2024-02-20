import pytest
from eight_queens import fitness_function

def test_fitness_function_correct_board():
    
    solution_board = '51842736'
    
    assert fitness_function(solution_board) == 28

def test_fitness_function_collisions():
    
    solution_board = '12341234'
    
    assert fitness_function(solution_board) == 10