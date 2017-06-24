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
import faceImport

#add_in = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0),(1,1,1)]
#add_out = [(0,0),(0,1),(0,1),(1,0),(0,1),(1,0),(1,0),(1,1)] #(co, out)
#global faceArr, moodArr, pairArr
faceArr = []
moodArr = []
pairArr = []

CPUpool = None

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
    #assert len(pairArr) > 0, 'No input data in child'
    global faceArr, moodArr, pairArr
    if len(moodArr)==0:
        print('Init worker thread')
        (faceArr,moodArr) = faceImport.faceReader('subset.csv')
        pairArr = list(zip(faceArr,moodArr))
    genome_id = genomeT[0]
    genome = genomeT[1]
    fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    for xi, xo in pairArr:
        output = net.activate(xi)
        for i in range(len(output)):
            fitness -= (output[i]- xo[i])**2
    fitness /= len(moodArr)
    return fitness
  
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

    # Run for up to ## generations.
    winner = p.run(eval_genomes, 30)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in pairArr:
        output = winner_net.activate(xi)
        print("expected output {!r}, got [".format(xo)+" ".join("%.1f" % x for x in output)+"]")
        #print("expected output {!r}, got {}".format(xo, output))

    #node_names = {-1:'A', -2: 'B', -3:'C_in', 0:'A+B', 1:'C_out'}
    #visualize.draw_net(config, winner, view=False, node_names=node_names)
    visualize.plot_stats(stats, ylog=True, view=False)
    visualize.plot_species(stats, view=False)

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-19')
    #p.run(eval_genomes, 10)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neatConfig.txt')
    (faceArr,moodArr) = faceImport.faceReader('subset.csv')
    pairArr = list(zip(faceArr,moodArr))
    print('Pairs: {}'.format(len(pairArr)))
    if CPUpool is None:
        CPUpool = mp.ProcessingPool(4)
    run(config_path)
    
    
    #cProfile.run('run(config_path)','runStat')
    #p = pstats.Stats('runStat')
    #p.sort_stats('tottime').print_stats()