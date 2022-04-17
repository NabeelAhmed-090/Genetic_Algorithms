import random
import string

POPULATION_SIZE = 10000
BEST_FIT = 0.1
CROSSOVER = 0.5
MUTATE = 0.4
POPULATION = []
BUFFER = []
TARGET = "Nabeel Ahmed"


class Sample:
    # class to store the sample string and associated value of the sample
    def __init__(self, sample="", value=9999):
        self.sample = sample
        self.value = value
    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value


def fitness_function(sample_str):
    # function to calculate the value of the sample string
    val = 0
    for i in range(len(TARGET)):
        val += abs(ord(sample_str[i]) - ord(TARGET[i]))
    return val


def generate_population():
    # helper function to generate population initially
    POPULATION.clear()
    BUFFER.clear()
    size = len(TARGET)
    for i in range(POPULATION_SIZE):
        # generating random string
        ran = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.whitespace, k=size))
        # calculating fitness value and storing it in population
        val = fitness_function(ran)
        sample_obj = Sample(ran, val)
        POPULATION.append(sample_obj)


def print_population():
    # helper function to print the population
    for i in range(POPULATION_SIZE):
        print(POPULATION[i].sample, " : ", POPULATION[i].value)


def filter_best_fit():
    # function to separate the fittest samples from the rest of the population
    BUFFER.clear()
    for i in range(int(BEST_FIT * POPULATION_SIZE)):
        BUFFER.append(POPULATION[i])


def apply_crossover():
    # function to apply crossover on random samples
    for i in range(int(CROSSOVER * POPULATION_SIZE)):
        # pick two parent samples at random
        parent_one = random.randint(0, POPULATION_SIZE // 2)
        parent_two = random.randint(parent_one, POPULATION_SIZE - 1)

        # find the substring indexes on which crossover has to be applied
        seperator_one = random.randint(0, len(TARGET))
        seperator_two = random.randint(seperator_one, len(TARGET))
        # applying crossover
        child_sample = ""
        child_sample += POPULATION[parent_one].sample[0:seperator_one:1]
        child_sample += POPULATION[parent_two].sample[seperator_one:seperator_two:1]
        child_sample += POPULATION[parent_one].sample[seperator_two:len(TARGET):1]
        # calculating fitness value and storing it in buffer
        val = fitness_function(child_sample)
        sample_obj = Sample(child_sample, val)
        BUFFER.append(sample_obj)


def mutate_population():
    # function to apply mutation on random samples
    for i in range(int(MUTATE * POPULATION_SIZE)):
        # pick the sample on which you need to apply mutation on
        mutation_sample = random.randint(0, POPULATION_SIZE - 1)
        # find the mutation indexes
        seperator_one = random.randint(0, len(TARGET))
        seperator_two = random.randint(seperator_one, len(TARGET))
        # applying mutation
        mutant = ""
        mutant += POPULATION[mutation_sample].sample[0:seperator_one:1]
        for j in range(seperator_one, seperator_two):
            mutant += chr(random.randint(0, 122) + 32)
        mutant += POPULATION[mutation_sample].sample[seperator_two:len(TARGET):1]
        # calculating fitness value and storing it in buffer
        val = fitness_function(mutant)
        sample_obj = Sample(mutant, val)
        BUFFER.append(sample_obj)


def buffer_to_population():
    # helper function to copy data from buffer to population
    POPULATION.clear()
    for i in range(POPULATION_SIZE):
        POPULATION.append(BUFFER[i])
    BUFFER.clear()


generate_population()
POPULATION.sort()
itr = 0

while POPULATION[0].value != 0 and itr < 1000:
    print(POPULATION[0].sample, " : ", POPULATION[0].value, " Iteration : ", itr)
    filter_best_fit()
    apply_crossover()
    mutate_population()
    buffer_to_population()
    POPULATION.sort()
    itr += 1

if POPULATION[0].value == 0:
    print("Target Reached : ", POPULATION[0].sample)
else:
    print("Iteration Limit Reached (Best Sample) : ", POPULATION[0].sample)
