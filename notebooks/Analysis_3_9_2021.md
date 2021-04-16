$$\Delta t_i = \gamma (y_i-p_i)$$
$$\Delta p_i = \delta (y_i-p_i)$$
$$\Delta q_{ij} = \beta y_i(x_j-q_{ij})$$
$$\Delta w_{ij} = -\alpha(y_iy_j-p_ip_j)$$

What I need is to keep $\sum q_i+\sum w_i = 1$, or at the very least $\sum q_i = 1$.

Also, I need $p_i=t_i$.

Idea 1:

Use $\Delta t_i = \Delta p_i = \delta (y_i-p_i)$, giving $t_i=p_i$. Also, use $q_{ij} = \beta y_i(x_jn-q_{ij})$, which should limit $q_{ij}$ to between $0$ and $n$, where $n$ is the average fraction of inputs that are on.

This doesn't really work, however, since the correct threshold value is not garunteed to be the same as the correct $p_i$ value.

Idea 2:

Use $t_i=p_i$ again, with $q_{ij} = \beta y_i(x_jp_i-q_{ij})$.