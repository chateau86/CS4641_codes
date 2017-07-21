#! python2
#Woradorn K.
import numpy as np
import subprocess
import multiprocessing as mp
import os
import time
varList = [
'node_add_prob',
'node_delete_prob',
'survival_threshold'
]
def runCase(d):
    print('start {}'.format(d))
    t = time.time()
    os.chdir(d)
    out = subprocess.check_output(['py','-2','NEAT_snake_test.py'])
    #print(out)
    fOut = open('test2log.txt','wb')
    fOut.write(out)
    fOut.close()
    os.chdir('../..')
    print('done {} in {:.2f} s'.format(d, time.time()-t))


#set up threadpool
if __name__ == '__main__':
    CPUpool = mp.Pool(processes=4)
    runList = []
    for var in varList:
        for val in np.arange(0,1.2,0.2):
            d = '{}/{:1.1f}'.format(var,val)
            runList.append(d)
        break
    CPUpool.map(runCase,runList)
            
            