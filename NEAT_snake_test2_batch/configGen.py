#! python2
#Woradorn K.
import numpy as np
import os
import shutil
varList = [
'node_add_prob',
'node_delete_prob',
'survival_threshold'
]

def genConfig(fInName, fOutName, varSub, varVal):
    fIn = open(fInName, 'r')
    fOut = open(fOutName, 'w')
    for line in fIn:
        if not line.startswith(varSub):
            fOut.write(line)
            #continue
        else:
            fOut.write('{} = {:1.1f}\n'.format(varSub, varVal))
    fIn.close()
    fOut.close()


for var in varList:
    try:
        os.mkdir(var)
    except:
        pass
    for val in np.arange(0,1.2,0.2):
        print('{}-{:1.1f}'.format(var,val))
        d = '{}/{}'.format(var,val)
        try:
            os.mkdir(d)
        except:
            pass
        genConfig('config-feedforward', '{}/config-feedforward'.format(d), var, val)
        #shutil.copy('original/*', d)
        for fn in os.listdir('original'):
            shutil.copy('original/{}'.format(fn), d)
        
        