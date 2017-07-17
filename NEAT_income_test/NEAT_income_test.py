

from __future__ import print_function
import os
import neat
import visualize
import pandas as pd
import numpy as np

#global numpy array
X = np.array([])
Y = np.array([])
X_test = np.array([])
Y_test = np.array([])
generation = 0

def initializeArrays():
    global X,Y
    data = pd.read_csv("training_preprocessed.csv", header=0)
    data.drop("Unnamed: 0", axis=1, inplace=True)
    Y = data.Prediction.values
    data.drop("Prediction", axis=1, inplace=True)
    X = data.values
    data2 = pd.read_csv("testing_preprocessed.csv", header=0)
    data2.drop("Unnamed: 0", axis=1, inplace=True)
    Y_test = data2.Prediction.values
    data2.drop("Prediction", axis=1, inplace=True)
    X_test = data2.values
    
    

def eval_genomes(genomes, config):
    global generation
    if len(X) == 0:
        initializeArrays()
    fitnessList = []
    for genome_id, genome in genomes:
        genome.fitness = 0.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(X,Y):
            output = net.activate(xi)
            genome.fitness -= (float(output - xo)) ** 2
        fitnessList.append(genome.fitness)
    maxIndex = fitnessList.index(max(fitnessList))
    filename_EG = 'best' + str(generation)
    winner_gid, winner_g = genomes[maxIndex]
    visualize.draw_net(config, winner_g, False, filename=filename_EG)
    generation += 1
    


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
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    winner_fitness = 0.0
    for xi, xo in zip(X_test, Y_test):
        output = winner_net.activate(xi)
        winner_fitness -= (float(output - xo)) ** 2
    print("Winner Testing Fitness: ")
    print(winner_fitness)    

    visualize.draw_net(config, winner, False, filename='WINNER_NET')
    visualize.plot_stats(stats, ylog=False)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
