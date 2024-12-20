import memory_profiler as mem_profile
import random
import time
from rich import print

names = ['John', 'Corey', 'Adam', 'Steve', 'Rick', 'Thomas']
majors = ['Math', 'Engineering', 'CompSci', 'Arts', 'Business']


def people_list(num_people):
    result = []
    for i in range(num_people):
        person = {
            'id': i,
            'name': random.choice(names),
            'major': random.choice(majors)
        }
        result.append(person)
    return result


def people_generator(num_people):
    for i in range(num_people):
        person = {
            'id': i,
            'name': random.choice(names),
            'major': random.choice(majors)
        }
        yield person


print('Memory (Before): {}Mb'.format(mem_profile.memory_usage()))
t1 = time.time()
people = people_list(1000000)
t1 = time.time()
print('Memory (Middle) : {}Mb'.format(mem_profile.memory_usage()))

t1 = time.time()
people = people_generator(1000000)
t1 = time.time()


print('Memory (After) : {}Mb'.format(mem_profile.memory_usage()))
#print ('Took {} Seconds'.format(t2-t1))
