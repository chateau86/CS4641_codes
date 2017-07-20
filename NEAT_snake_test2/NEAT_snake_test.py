

from __future__ import print_function
import os
import neat
import visualize
import pandas as pd
import numpy as np
import game
import pickle

#global numpy array
generation = 0
seeder = 0
mappingOut = {0:-1, 1:0, 2:1}

def lookList(tuple1):
    inList = []
    matrix = tuple1[0]
    for outside in matrix:
        for inside in outside:
            inList.append(inside)    
    return inList + list(tuple1[1])

def storeGS(gameState, filename):
    with open(filename, 'wb') as output:
        pickle.dump(gameState, output, pickle.HIGHEST_PROTOCOL)

def storeNN(net, filename):
    with open(filename, 'wb') as output:
        pickle.dump(net, output, pickle.HIGHEST_PROTOCOL)

def storeMoves(moves, filename):
    thefile = open(filename, 'w')
    for ele in moves:
        thefile.write(str(ele) + '\n')    
    
def eval_genomes(genomes, config):
    global generation, seeder, mappingOut
    fitnessList = []
    moves = []
    for genome_id, genome in genomes:
        genome.fitness = 0.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        gS = game.gameState(w=8, h=8, seed=seeder, timeLimit=30)
        contLoop = True
        score = 0
        genomeMove = []
        while contLoop:
            xi = lookList(gS.look())       
            output = net.activate(xi) #indices 0->-1, 1->0, 2->1
            output = list(output)
            chosenOut = output.index(max(output))
            chosenOut = mappingOut[chosenOut]
            genomeMove.append(int(chosenOut))
            try:
                score = gS.run(chosenOut)
            except:
                contLoop = False
  
        genome.fitness = score
        fitnessList.append(genome.fitness)
        moves.append(genomeMove)
    maxIndex = fitnessList.index(max(fitnessList))
    print('Max fitness:')
    print(max(fitnessList))
    filename_EG = 'best' + str(generation)
    filename_GS = 'gS' + str(seeder)
    filename_NN = 'NN' + str(seeder)
    filename_M = 'moves' + str(seeder)
    recordGS = game.gameState(w=8,h=8, seed=seeder,timeLimit=30)
    storeGS(recordGS, filename_GS)
    bestMoves = moves[maxIndex]
    storeMoves(bestMoves, filename_M)
    
    winner_gid, winner_g = genomes[maxIndex]
    #netS = neat.nn.FeedForwardNetwork.create(winner_g, config)
    storeNN(winner_g, filename_NN)
    
    visualize.draw_net(config, winner_g, False, filename=filename_EG)
    generation += 1
    seeder += 1
    


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

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

    visualize.draw_net(config, winner, False, filename='WINNER_NET')
    visualize.plot_stats(stats, ylog=False)
    visualize.plot_species(stats, view=True)



if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
