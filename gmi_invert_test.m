load("design_matrix_shcoeff.mat")

A_sh = A_sh_fromfile.';


sigma_d = 0.01;
sigma_x = 0.01;

A_T = A_sh.';
M = A_T;

n_bodies = length(A_T(:, 1))
n_points = length(A_T(1, :))

COV_d = eye(n_points)*(sigma_d^2);
P = inv(COV_d);

COV_x = eye(n_bodies)*(sigma_x^2);
Q = inv(COV_x);

A_TP = A_T*P;
A_TPA = A_TP*A_sh;

A_TPApQ_inv = inv(A_TPA + Q);

A_TPd = A_TP * d_sh';
M = Q*(ones(n_bodies)'*0.02);

M
A_TPdpQx0 = A_TPd + Q*(ones(n_bodies)*0.02);


stop
disp(M)

disp(M(1, 1))
disp(M(end, end))
disp(M(1, end))
disp(M(end, 1))

h = A_TPApQ_inv * A_TPdpQx0;

