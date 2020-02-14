
def nlssubprob(V, W, Hinit, tol, maxiter):
    # NMF by alternative non-negative least squares using projected gradients
    # Author: Chih-Jen Lin, National Taiwan University

    # W,H: output solution
    # Winit,Hinit: initial solution
    # tol: tolerance for a relative stopping condition
    # timelimit, maxiter: limit of time and iterations

        # H, grad:output solution and gradient
    # iter:#iterations used
    # V, W: constant matrices
    # Hinit: initial solution
    # tol: stopping tolerance
    # maxiter: limit of iterations

    import numpy as np

    H = Hinit

    WtV=np.dot(np.transpose(W),V)
    WtW=np.dot(np.transpose(W),W)

    alpha=1
    beta=0.1

    print('tol: ' + str(tol))
    print('Maximum iterations: ' + str(maxiter))
    #from tqdm import tqdm

    logfile = open('nlssubprob.dat', 'w')
    for iter in range(maxiter):

        grad = np.dot(WtW,H) - WtV
        #show_matrix_corners(grad)

        projgrad=np.linalg.norm(grad[((grad < 0) | (H > 0))])
        print ("Iteration " + str(iter) + " projgrad: " + str(projgrad))
        logfile.write(str(iter) + ' ' + str(projgrad) + '\n')

        if projgrad < tol:
            break
        for inner_iter in range(20):
            Hn = np.maximum(H - np.dot(alpha,grad), 0)
            d = Hn - H

            gradd=np.sum(np.sum(np.multiply(grad,d)))
            dQd=np.sum(np.sum(np.multiply((np.dot(WtW,d)),d)))

            suff_decr=(0.99*gradd + 0.5*dQd) < 0
            if inner_iter==0:
                decr_alpha = ~suff_decr
                Hp = H
            if decr_alpha:
                if suff_decr:
                    H = Hn
                    break
                else:
                    alpha = alpha * beta;

            else:
                if ((~suff_decr) | np.array_equal(Hp, Hn)):
                    H = Hp
                    break
                else:
                    alpha = alpha/beta
                    Hp = Hn
        #if iter==maxiter-1:
            #print("Max iter in nlssubprob")

    logfile.close()
    return H

def nlssubprob_plt(V, W, Hinit, tol, maxiter):
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    import gmi_misc
    import os

    matplotlib.use("Qt5agg")
    plt.style.use('ggplot')

    H = Hinit

    H_flat = H.flatten()
    xd, yd, grid = gmi_misc.write_sus_grid_to_file(H_flat, 'dummy')


    plt.ion()
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.title.set_text('Current solution h, iteration n = ' + str(0))

    im = ax.imshow(grid, interpolation='nearest',
                                origin='bottom',
                                aspect='auto', # get rid of this to have equal aspect
                                vmin=0.0,
                                vmax=0.1,
                                cmap='jet')

    ax.set_xticks(np.arange(0, len(grid[0, :])+1, len(grid[0, :])/6), minor=False)
    ax.set_xticklabels(np.arange(-180, 180+1, 60).astype(str), fontdict=None, minor=False)
    ax.set_xlabel('lon [deg]')

    ax.set_yticks(np.arange(0, len(grid[:, 0])+1, len(grid[:, 0])/6), minor=False)
    ax.set_yticklabels(np.arange(-90, 90+1, 30).astype(str), fontdict=None, minor=False)
    ax.set_ylabel('lat [deg]')

    cb = plt.colorbar(im)
    plt.draw()
    plt.show()


    WtV=np.dot(np.transpose(W),V)
    WtW=np.dot(np.transpose(W),W)

    alpha=1
    beta=0.1

    print('tol: ' + str(tol))
    print('Maximum iterations: ' + str(maxiter))
    #from tqdm import tqdm

    import os
    try:
        os.mkdir('video')
    except:
        print('nothing')

    logfile = open('nlssubprob.dat', 'w')
    for iter in range(maxiter):
        H_flat = H.flatten()
        xd, yd, grid2 = gmi_misc.write_sus_grid_to_file(H_flat, 'dummy')
        im.set_data(grid2)

        ax.title.set_text('Current solution h, iteration n = ' + str(iter))

        plt.draw()

        fig.canvas.start_event_loop(0.0001)


        grad = np.dot(WtW,H) - WtV

        projgrad=np.linalg.norm(grad[((grad < 0) | (H > 0))])
        print ("Iteration " + str(iter) + " projgrad: " + str(projgrad))
        logfile.write(str(iter) + ' ' + str(projgrad) + '\n')
        plt.savefig('video/iteration_' + str(iter) + '.png')

        if projgrad < tol:
            break
        for inner_iter in range(20):
            Hn = np.maximum(H - np.dot(alpha,grad), 0)
            d = Hn - H

            gradd=np.sum(np.sum(np.multiply(grad,d)))
            dQd=np.sum(np.sum(np.multiply((np.dot(WtW,d)),d)))

            suff_decr=(0.99*gradd + 0.5*dQd) < 0
            if inner_iter==0:
                decr_alpha = ~suff_decr
                Hp = H
            if decr_alpha:
                if suff_decr:
                    H = Hn
                    break
                else:
                    alpha = alpha * beta;

            else:
                if ((~suff_decr) | np.array_equal(Hp, Hn)):
                    H = Hp
                    break
                else:
                    alpha = alpha/beta
                    Hp = Hn
        #if iter==maxiter-1:
            #print("Max iter in nlssubprob")


    logfile.close()
    plt.close()


    if os.path.exists("video_log.mp4"):
        os.remove("video_log.mp4")
    else:
        print("video_log.mp4 does not exist")

    os.system('ffmpeg -framerate 2 -i "video/iteration_%d.png" video_log.mp4')


    import shutil
    try:
        shutil.rmtree("video")
    except:
        print("no video dir")


    return H

