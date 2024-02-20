import random

class Board:
    config = ''
    fitness = 0
    
    def create_board(self):
        """ 
        Funciton to create a random board configuration

        Returns:
            string: 8 Queens board configuration
        """
        for i in range(0,8,1):
            current = str(random.randint(1,8))
            self.config += current
    
    def update_board(self, new_board):
        self.config = new_board    

    def fitness_function(self):
        """
        Function to determine the number of mutually attacking queens, then subtract
        from 28 (the max possible)

        Args:
            board str: 8 queens board

        Returns:
            int: score
        """
        total_score = 0
        for i in range(0,len(self.config), 1):
            for j in range( (i + 1) , len(self.config), 1):
                if self.config[i] == self.config[j]: # Same row 
                    total_score += 1
                # print(f'A - i is {board[i]}, j is {board[j]}')
                elif int(self.config[j]) == (int(self.config[i]) + (j - i)): # diagonal up
                    total_score += 1
                    
                    #print(f'B - i is {board[i]}, j is {board[j]}, board i + j is {int(board[i]) + (j-i)}')
                elif int(self.config[j]) == (int(self.config[i]) - (j-i)): # diagonal down
                    total_score += 1
                    #print(f'C - i is {board[i]}, j is {board[j]}')
        
        self.fitness = 28 - total_score
    
    def print_board(self):
        print(f'Configuration: {self.config}, Fitness: {self.fitness}')



def create_population(size):
    population = [Board() for i in range(size)] 
    for i in range(0, size, 1):
        population[i].create_board()
        population[i].fitness_function()
    return population

def update_population(child_list, population):
    for i in range(0, len(population), 1):
        population[i].update_board(child_list[i])
        population[i].fitness_function()
    return population

def solution_found(population):
    for i in range(0, len(population), 1):
        if population[i].fitness == 28:
            return population[i].config
    return False

def display_population(population, size):
    for i in range(0, size, 1):
        print(i, end=' ')
        population[i].print_board()
    print('Average Fitness = ', average_fitness(population, size))
    
def sum_fitness(population):
    total_fitness = 0
    for i in range(0, len(population), 1):
        total_fitness += population[i].fitness
    return total_fitness

def average_fitness(population, size):
    average = float(sum_fitness(population))/float(size)
    return average

def crossover(parent1:str, parent2:str):
    crossover_point = random.randint(1,7)
    #print(f'crossover point = {crossover_point}')
    child1 = ''
    child2 = ''
    for i in range(0, crossover_point, 1):
        child1 += parent1[i]
        child2 += parent2[i]
    for j in range(crossover_point, 8, 1):
        child1 += parent2[j]
        child2 += parent1[j]
    return [child1, child2]

def create_probability_list(population, size):
    probability_list = {}
    total_fitness = sum_fitness(population) 
    previous = 0
    for i in range(0, len(population), 1):
        percentage = previous + (100 * (float((population[i].fitness)) / float(total_fitness)))
        previous = percentage
        probability_list[i] = percentage
    return probability_list

def select_parents(population, probability_list, size):
    parent_list = []
    for i in range(0, size, 1):
        if (i % 2) == 1:
            parent_list.append(population[random.randint(0,size-1)].config)
        else:
            percentile = random.randint(0, 100)
            j = 0
            match_found = False
       
            while j < size and not match_found:
                if (percentile <= probability_list[0]):
                    parent_list.append(population[0].config)
                    match_found = True
                    
                elif (percentile > probability_list[j]) and (percentile <= probability_list[j+1]):
                    parent_list.append(population[j+1].config)
                    match_found = True
                    
                elif (percentile >= probability_list[size-1]):
                  
                    parent_list.append(population[size-1].config) 
                    match_found = True
                else:
                    j += 1
              
    return parent_list

def create_child_list(parents):
    child_list = []
    mutation_dice = random.randint(1,2) 
    for i in range(0, len(parents), 2):
        current_children = crossover(parents[i], parents[i+1])
        child_list.append(current_children[0])
        child_list.append(current_children[1])
        current_children = []
    if mutation_dice == 2:
        index_to_mutate = random.randint(0,len(child_list) - 1)
        child_list[index_to_mutate] = mutate(child_list[index_to_mutate])
    return child_list

def mutate(to_mutate):
    
    print(f'Mutate {to_mutate}')
    digit_to_mutate = random.randint(0,9)
    new_child = ''
    for i in range(0, len(to_mutate), 1):
        if i != digit_to_mutate:
            new_child += to_mutate[i]
        else:
            new_child += str(random.randint(1,8))
        #print(f'New child = {new_child}')
    return new_child
        
# Set population size
populationSize = 100

# generate initial population
population = create_population(populationSize)

display_population(population, populationSize)
runs = 0
solution = False
while runs < 2000 and not solution:
    solution = solution_found(population) 
    if not solution:
        total_fitness = sum_fitness(population)
        probability_list = create_probability_list(population, populationSize)
        #print(f'Total fitness = {total_fitness}')
        #print(probability_list)

        parents = select_parents(population, probability_list, populationSize)
        #print('parents', parents)
        children = create_child_list(parents)
        #mutate(children)
        #print('children', children)
        population = update_population(children, population)
        print('Runs = ', (runs + 1))
        display_population(population, populationSize)
        runs += 1
    else:
        print(f'Solution Found! After {runs} iterations, {solution} solves the 8 queens problem')

#print(crossover(initial_population[0], initial_population[1]))
#print(max(initial_population, key=initial_population.get))
#print(initial_population)
#print(board)

#solution_board = '51842736'

#print(solution_board)
#score = fitness_function(board)

#print(score)
    
    
    