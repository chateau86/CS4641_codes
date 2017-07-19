#! python2
#Woradorn K.
import game
import matplotlib.animation as mpa
import matplotlib.pyplot as plt
def animate(g, moveArr, fName):
    #Input: 
    #   g: Game state initialized the same way as on the recorded run
    #   moveArr: List of moves for the whole game
    #   fName: Output file name
    
    Writer = mpa.writers['ffmpeg']
    writer = Writer(fps=15)
    fig = plt.figure()
    plt.axis([0, g._gridSize[0], 0, g._gridSize[1]])
    im = []
    im.append([plt.imshow(g.gameGrid, 
        interpolation='none', 
        origin='upper',
        extent = [0, g._gridSize[0], 0, g._gridSize[1]],
        cmap = 'seismic',
        vmin=-4, vmax=4)])
    #plt.show()
    for m in moveArr:
        #print('move: {}'.format(m))
        g.run(m)
        #plt.grid(True)
        im.append([plt.imshow(g.gameGrid, 
            interpolation='none', 
            origin='upper',
            extent = [0, g._gridSize[0], 0, g._gridSize[1]],
            cmap = 'seismic',
            vmin=-4, vmax=4)])
        #plt.show()
    im_ani = mpa.ArtistAnimation(fig, im, interval=500, blit=True)
    #plt.grid(True)
    im_ani.save(fName)
    #plt.show()
    
