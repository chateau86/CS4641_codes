#! python3
#Woradorn K.
import numpy as np
def dump_stats(statistics, fName):
    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())
    dataOut = zip(generation,best_fitness,avg_fitness,stdev_fitness)
    fOut = open(fName,'w')
    fOut.write('gen, best, avg, stdev\n')
    for line in dataOut:
        fOut.write('{}, {}, {}, {}\n'.format(line[0],line[1],line[2],line[3]))
    fOut.close()
    
def dump_species(statistics, fName):
    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    gen = range(num_generations)
    curves = np.array(species_sizes).T
    dataOut = zip(gen, species_sizes, curves)
    fOut = open(fName,'w')
    fOut.write('gen, species_sizes, curves\n')
    for line in dataOut:
        #print('{}, {}, {}\n'.format(line[0],line[1],line[2]))
        fOut.write('{}, {}, ['.format(line[0],line[1]) + " ".join("%.1f" % x for x in line[2])+"]")
        
    fOut.close()