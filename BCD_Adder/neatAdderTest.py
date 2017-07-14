#! python3
#Woradorn K.
import neat
import os
import visualize
import cProfile
import pstats
import numpy as np
import collections
import pathos.multiprocessing as mp

import dataGen

CPUpool = None

add_in = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0),(1,1,1)]
add_out = [(0,0),(0,1),(0,1),(1,0),(0,1),(1,0),(1,0),(1,1)] #(co, out)
pairArr = list(zip(add_in,add_out))
#def eval_genomes(genomes, config):
#    for genome_id, genome in genomes:
#        genome.fitness = 8.0
#        net = neat.nn.FeedForwardNetwork.create(genome, config)
#        for xi, xo in zip(add_in, add_out):
#            output = net.activate(xi)
#            genome.fitness -= (output[0] - xo[0])**2+(output[1] - xo[1])**2

def eval_genomes(genomes, config):
    assert len(pairArr) > 0, 'No input data in main thread'
    print('Pair: {}'.format(len(pairArr)))
    #collections.deque(map(lambda genomeT: eval_single(genomeT, config), genomes),0)
    assert CPUpool is not None, "CPUpool empty"
    fList = CPUpool.map(lambda genomeT: eval_single(genomeT, config), genomes)
    #heavy lifting done
    for genomeT, fit in zip(genomes, fList):
        genomeT[1].fitness = fit

def eval_single(genomeT, config):
    genome_id = genomeT[0]
    genome = genomeT[1]
    genome.fitness = 8.0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    for xi, xo in zip(add_in, add_out):
        output = net.activate(xi)
        genome.fitness -= (output[0] - xo[0])**2+(output[1] - xo[1])**2
    return genome.fitness
            
def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(20))

    # Run for up to 500 generations.
    winner = p.run(eval_genomes, 500)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(add_in, add_out):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {-1:'A', -2: 'B', -3:'C_in', 0:'A+B', 1:'C_out'}
    visualize.draw_net(config, winner, view=False, node_names=node_names)
    visualize.plot_stats(stats, ylog=True, view=False)
    visualize.plot_species(stats, view=False)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-19')
    p.run(eval_genomes, 10)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neatConfig.txt')
    if CPUpool is None:
        CPUpool = mp.ProcessingPool(3)
    run(config_path)
    #cProfile.run('run(config_path)','runStat')
    #p = pstats.Stats('runStat')
    #p.sort_stats('tottime').print_stats()