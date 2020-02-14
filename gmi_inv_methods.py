

#Generalized Tikhonov
def Generalized_Tikhonov(A, d, sigma_d, sigma_x, x_0):
    print("Generalized Tikhonov inversion")
    import time
    start = time.time()

    import numpy as np

    A_T = np.transpose(A)

    n_bodies = len(A_T[:, 0])
    print("  Number of bodies: " + str(n_bodies))
    n_points = len(A_T[0, :])
    print("  Number of datapoints: " + str(n_points))

    print("  Variance of data: " + str(sigma_d))
    print("  Variance of susceptibility: " + str(sigma_x) + " SI")
    print("  A-priori susceptibility: " + str(x_0) + " SI")

    #print str(n_bodies)
    #print str(n_points)


    COV_d = np.dot(np.identity(n_points), (sigma_d*sigma_d))
    P = np.linalg.inv(COV_d)
    COV_x = np.dot(np.identity(n_bodies), (sigma_x*sigma_x))
    Q = np.linalg.inv(COV_x)

    A_TP = np.dot(A_T, P)
    A_TPA = np.dot(A_TP, A)

    A_TPApQ_inv = np.linalg.inv(np.add(A_TPA, Q))

    A_TPd = np.matmul(A_TP, d)

    col = np.matmul(Q, x_0)
    A_TPdpQx0 = np.add(A_TPd, col)

    h = np.matmul(A_TPApQ_inv, A_TPdpQx0)

    end = time.time()
    print("  Time spent: " + str(end - start) + " sec")
    print(str(h))
    return h


#L2 minimization
def L2_minimization(A, d, alpha):
    print("L2 minimization")
    import time
    start = time.time()

    import numpy as np

    A_T = np.transpose(A)
    ATA = np.dot(A_T, A)
    ATA_inv = np.linalg.inv(np.add(ATA, np.identity(len(ATA))*alpha**2))
    L = np.dot(ATA_inv, A_T)
    h = np.dot(L, d)

    end = time.time()
    print("  Time spent: " + str(end - start) + " sec")
    print(str(h))
    return h


def Projected_Gradient(A, d, x_0):
    import gmi_config
    gmi_config.read_config()

    print("Projected Gradient inversion")
    import time
    start = time.time()

    import numpy as np

    d_col = d[:, np.newaxis]

    n_bodies = len(A[0, :])

    #x_0vect = (np.ones(n_bodies)*x_0)
    x_0col = x_0[:, np.newaxis]

    import nlssubprob
    h = nlssubprob.nlssubprob_plt(d_col,A,x_0col,1e-6,gmi_config.MAX_ITER)

    end = time.time()
    print("  Time spent: " + str(end - start) + " sec")

    h = h.flatten()

    return h

