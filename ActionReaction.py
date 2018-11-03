import os, sys, networkx as nx, numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi

neighb = [[1,1,1],
          [1,0,1],
          [1,1,1]]


class agent:

    position = []
    endpoint = []
    x = 0
    y = 0

    motion_percept = {}
    position_weights = {}

    value = 0
    Map = object

    def __init__(self, where, what, world):
        self.position = where
        self.value = what
        self.Map = world

    def summary(self):
        print "Agent @ "+str(self.position)
        print "Value: "+str(self.value)

    def crawl_space(self, target):
        if target[0] <= self.Map.manifold.shape[0] and target[1] <= self.Map.manifold.shape[1]:
            self.endpoint = target
        else:
            print "Target Point is out of bounds!"
            exit(0)
        x = self.position[0]
        y = self.position[1]
        self.motion_percept = {'U': [x, y + 1],
                          'D': [x, y - 1],
                          'L': [x - 1, y],
                          'R': [x + 1, y]}

        # Now Crawl the space.manifold to the target,
        # only following paths of matching boolean values
        moves = self.Map.agent_density
        state = moves[self.position[0], self.position[1]]
        best_move = 0
        direction = ''
        print "STATE: "+str(state)
        try:
            u = self.motion_percept['U']
            up = moves[u[0],u[1]]
            self.position_weights['U'] = up
        except IndexError:
            pass
        try:
            dwn = self.motion_percept['D']
            down = moves[dwn[0],dwn[1]]
            self.position_weights['D'] = down
        except IndexError:
            pass
        try:
            lft = self.motion_percept['L']
            left = moves[lft[0],lft[1]]
            self.position_weights['L'] = left
        except IndexError:
            pass
        try:
            rt = self.motion_percept['R']
            right = moves[rt[0],rt[1]]
            self.position_weights['R'] = right
        except IndexError:
            pass

        for key in self.position_weights:
            if self.position_weights[key] > best_move:
                best_move = self.position_weights[key]
                direction = key
        print self.position_weights
        print "Best Move is "+direction
        return direction


class space:

    bounds = []
    ratio_filled = 0
    manifold = [[]]
    agent_density = [[]]

    def __init__(self, x0, x1, y0, y1, mixture, debug):
        self.bounds = [x0, x1, y0, y1]
        self.ratio_filled = mixture

        # Populate the manifold of space
        dx = abs(x1-x0)
        dy = abs(y1-y0)
        self.manifold = np.random.randint(0,255,dx*dy,dtype=int).reshape((dx,dy)) > mixture
        # Create a map  of neighbor density for an agent to navigate
        self.agent_density = ndi.convolve(np.array(self.manifold, dtype=int), neighb, origin=0)

        if debug:
            self.show_space()

    def show_space(self):
        plt.imshow(self.manifold,'gray_r')
        plt.show()
        plt.imshow(self.agent_density,'gray_r')
        plt.show()


def main():
    # Dense Space
    dense_void = space(0, 100, 0, 100, 70, True)

    # Sparse Space
    mostly_empty = space(0, 100, 0, 100, 200, True)

    # Create an agent to navigate a space
    position = [0,0]
    ai = agent(position,mostly_empty.manifold[0,0],mostly_empty)
    ai.summary()
    next = ai.crawl_space([50,50])
    position = ai.motion_percept[next]
    print "New Position @ "+str(position)

if __name__ == '__main__':
    main()
