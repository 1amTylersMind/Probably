import sys, os, numpy as np, scipy.ndimage as ndi
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.ndimage.interpolation import zoom

def apply_sigmoid(imat):
    return -np.log(1/((1 + imat)/255)-1)


def undo_sigmoid(imat):
    return (1+1/(np.exp(-imat) + 1)*255).astype("uint8")


def kmeans(imat):
    im_small = zoom(imat, (0.2, 0.2, 1))
    h, w = im_small.shape[:2]
    im_small_long = im_small.reshape((h * w, 3))
    km = KMeans(n_clusters=3)
    km.fit(im_small_long)

    # Find Clusters
    cc = km.cluster_centers_.astype(np.uint8)
    out = np.asarray([cc[i] for i in km.labels_]).reshape((h,w,3))

    # Put together into segments
    seg = np.asarray([(1 if i == 1 else 0)
                      for i in km.labels_]).reshape((h, w))
    fig, ax = plt.subplots(1,3)
    ax[0].imshow(imat)
    ax[0].set_xlabel('Original')
    ax[1].imshow(out)
    ax[1].set_xlabel('Clustered Filtering')
    ax[2].imshow(seg)
    ax[2].set_xlabel('KMeans Segments')
    plt.show()
    return seg


def create_grid():
    black = np.zeros((3,3,3))
    white = np.ones((3,3,3))
    whiteRow = np.concatenate((white,white,white,white,white,white),0)
    blackRow = np.concatenate((black,black,black,black,black,black),0)
    checkRow = np.concatenate((white,black,white,black,white,black),0)
    checkR0w = np.concatenate((black,white,black,white,black,white),0)
    gridLU = np.concatenate((blackRow,checkR0w,blackRow,checkR0w,blackRow,checkR0w),1)
    gridLD = np.concatenate((blackRow,checkRow,blackRow,checkRow,blackRow,checkRow),1)
    gridRU = np.concatenate((checkR0w,blackRow,checkR0w,blackRow,checkR0w,blackRow),1)
    gridRD = np.concatenate((checkRow,blackRow,checkRow,blackRow,checkRow,blackRow),1)
    gridR = np.concatenate((gridRU,gridRD),0)
    gridL = np.concatenate((gridLU,gridLD),0)
    GRID = np.concatenate((gridL,gridR),1)
    centRow = np.concatenate((whiteRow,whiteRow,blackRow,blackRow,whiteRow,whiteRow),1)
    checker = np.concatenate((checkRow,checkR0w,checkRow,checkR0w,checkRow,checkR0w),1)

    print "centrow "+str(centRow.shape)
    print "checker "+str(checker.shape)
    print "grid "+str(GRID.shape)

    plt.imshow(GRID)
    #plt.show()
    return GRID


def create_swarm():
    data = []
    noise = np.random.randint(0,2,765)
    deg = 0
    for pt in noise:
        data.append(np.float32(pt))
        deg += 1
    imat = np.concatenate((data,data,data,data),0).reshape((34,30,3))
    plt.imshow(imat)
    plt.show()
    return imat


def main():
    if '-read' in sys.argv:
        try:
            matrix = np.array(plt.imread(sys.argv[2]))
            kmeans(matrix)
        except IndexError:
            print "Incorrect Usage!"
            exit(0)
    if '-space' in sys.argv:
        hubble = '/usr/local/lib/python2.7/dist-packages/skimage/data/hubble_deep_field.jpg'
        kmeans(plt.imread(hubble))
    if '-check' in sys.argv:
        try:
            plt.imshow(plt.imread(sys.argv[2]))
            plt.show()
        except IndexError:
            exit(0)
            s = kmeans(plt.imread(sys.argv[2]))
            print s
    if '-grid' in sys.argv:
        matrix = create_grid()
        kmeans(matrix)
    if '-test' in sys.argv:
        matrix = create_swarm()
        print matrix.shape
        s = kmeans(matrix)


if __name__ == '__main__':
    main()
