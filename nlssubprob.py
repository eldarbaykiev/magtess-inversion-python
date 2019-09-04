
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

    for iter in range(maxiter):
        grad = np.dot(WtW,H) - WtV
        #show_matrix_corners(grad)

        projgrad=np.linalg.norm(grad[((grad < 0) | (H > 0))])
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
        if iter==maxiter-1:
            print "Max iter in nlssubprob"

    return H
