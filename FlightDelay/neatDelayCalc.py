#! python3
#Woradorn K.

#Subsample image to 24*24
import neat
import os
import visualize
import cProfile
import pstats
import numpy as np
import collections
import pathos.multiprocessing as mp
import fileSampler

dataArr = []

CPUpool = None
buckets = 5

setNum = 0
def eval_genomes(genomes, config):
    global setNum
    assert len(dataArr) > 0, 'No input data in main thread'
    print('run with set {}'.format(setNum))
    print('Pair: {}'.format(len(dataArr[setNum])))
    #collections.deque(map(lambda genomeT: eval_single(genomeT, config), genomes),0)
    assert CPUpool is not None, "CPUpool empty"
    fList = CPUpool.map(lambda genomeT: eval_single(genomeT, config, setNum), genomes)
    setNum += 1
    setNum %= buckets
    #heavy lifting done
    for genomeT, fit in zip(genomes, fList):
        genomeT[1].fitness = fit
    
def eval_single(genomeT, config, setNum):
    #assert len(pairArr) > 0, 'No input data in child'
    global dataArr
    if len(dataArr)==0:
        print('Init worker thread')
        dataArr = fileSampler.sample('dataOut.csv', buckets)
    genome_id = genomeT[0]
    genome = genomeT[1]
    fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    #for xi, xo in dataArr[setNum]:
    for ind in range(len(dataArr[setNum][0])):
        xi = dataArr[setNum][0][ind]
        xo = dataArr[setNum][1][ind]
        output = net.activate(xi)[0]
        fitness -= abs(output - xo)
    fitness /= len(dataArr[setNum][0])      
    return fitness
  
def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    #uncomment to resume
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-279')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    node_names = {
        -1:'hour',
        -2: 'windN',
        -3:'windE',
        -4:'gust',
        -5:'vis',
        -6:'cloud',
        -7:'temp',
        -8:'dew',
        -9:'baro',
        -10:'flightRate',
        0:'Delay' 
    }

    for i in range(100):
        # Run for up to ## generations.
        winner = p.run(eval_genomes, 10)
        print('visualizing stats')
        visualize.draw_net(config, winner, view=False,  node_names=node_names)
        #visualize.plot_stats(stats, ylog=True, view=False)
        #visualize.plot_species(stats, view=False)
        print('done drawing graph')
    # Display the winning genome.
    
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    fitness = 0
    for ind in range(len(dataArr[buckets][0])):
        xi = dataArr[buckets][0][ind]
        xo = dataArr[buckets][1][ind]
        output = winner_net.activate(xi)
        print("expected output {:.4f}, got [".format(xo)+" ".join("%.4f" % x for x in output)+"]")
        fitness -= (output[0] - xo)**2
    fitness /= len(dataArr[buckets][0])  
    print('Winner fitness = {:.2f}'.format(fitness))
        #print("expected output {!r}, got {}".format(xo, output))


    visualize.draw_net(config, winner, view=False, node_names=node_names)
    visualize.plot_stats(stats, ylog=True, view=False)
    visualize.plot_species(stats, view=False)

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-19')
    #p.run(eval_genomes, 10) #This runs a few more generations of NN from checkpoint

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neatConfig_ss2.txt')
    dataArr = fileSampler.sample('dataOut.csv', buckets)
    if CPUpool is None:
        CPUpool = mp.ProcessingPool(4)
    run(config_path)
    
    
    #cProfile.run('run(config_path)','runStat')
    #p = pstats.Stats('runStat')
    #p.sort_stats('tottime').print_stats()