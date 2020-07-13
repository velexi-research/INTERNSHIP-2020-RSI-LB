<script src="https://polyfill.io/v3/polyfill.min.js?features=es6">

</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">

</script>

ox2020-07-11: Analysis of Learning Update Equations
-------------------------------------------------

*Author*: Kevin Chu `<kevin@velexi.com>`

*Last Updated*: 2020-07-12

-------------------------------------------------------------------------------

Preface
-------

* This document is written using GitHub Markdown and uses LaTex to express
  math equations. It is best viewed using a Markdown viewer that supports
  GitHub Markdown and LaTeX rendering (e.g., using MathJax).

  * [Chrome Markdown Viewer][chrome-markdown-viewer]

    * _Note_: be sure to enable the following extension settings

      * Automatically allow access on the following sites
        * `file:///*`

      * Allow access to file URLS

      * Enable `mathjax`

-------------------------------------------------------------------------------

### Context

In his computational experiments, Luke has observed that convergence of node
threshold values is sensitive to the choice of the bit probability $p_i$ set
for each node. This observation prompted a deeper mathematical analysis of the
update algorithms.

### 1. Potential problems with the Foldiak algorithm learning rules

#### The theshold update equation converges only when $E[y_i] \rightarrow p_i$

Let $t_i^s$ denote the threshold for the $i$-th node after $s$ learning cycles.
Noting that $\Delta t_i^s = t_i^s - t_i^{s-1}$, the Foldiak's threshold update
equation may be expressed as

\[
  \Delta t_i^s = t_i^s - t_i^{s-1}
  = \gamma (y_i^s (\mathbf{Q}, \mathbf{W}, \mathbf{t}) - p_i),
\]

where the dependence of $y_i^s$ on the learned memories, inhibition weights,
the node thresholds, and learning cycle index have been made explicit.

Summing over $s$, we can derive the following expression for $t_i^s$:

\[
  t_i^s - t_i^0
  = \sum_{\tau = 1}^s \Delta t_i^\tau
  = \gamma \sum_{\tau = 1}^s (y_i^\tau- p_i)
  = \gamma s \left[ \left(
                      \frac{1}{s} \sum_{\tau = 1}^s y_i^\tau
                    \right)
                  - p_i
             \right].

\]

Note that if the expected value of $y_i$ exists, the sum approaches $E[y_i]$.

___Relevant Cases___

* $E[y_i] = p_i$. In this case, the limit on the right-hand side is
  indeterminate, so it can approach any value. Computational experiments
  indicate that $t_i^s$ approaches a constant when $p_i$ is set to $E[y_i]$,
  which suggests that

  \[
    E \left[ \frac{1}{s} \sum_{\tau = 1}^s y_i^{\tau} \right] - p_i
    \approx \frac{\alpha}{s} + \textrm{(higher-order terms)}.
  \]

  __Note__: it might be possible to prove this relation and determine $\alpha$
  from theoretical convergence rates for the law of large numbers, but I don't
  know the convergence rate results of the top of my head (and didn't find
  them from a quick internet search).

* $E[y_i] \ne p_i$. The right-hand side tends towards

  \[
    \gamma (E[y_i] - p_i) s,
  \]

  so the threshold value is expected to tend towards a linear function of $s$.

___Observations___

* The computational experiments suggest that the key error approaches a
  constant value as $s \rightarrow \infty$. Therefore, it seems reasonable to
  assume that $y_i$ has a finite expected value.

* Note that the contribution of the initial threshold value does not
  automatically vanish as $s \rightarrow \infty$. We need to rely on the
  expectation value of $y_i$ to be equal to $p_i$.

#### The inhibition weight and threshold update equation behave similarly

* An analysis of the inhibition equation using the same approach as for the
  threshold equation leads to similar conclusions for the inhibition weights.

* The conditions required for convergence of the inhibition weights are:

  * $E[y_i] = p_i$ for all $i$

  * $Cov(y_i, y_j) = 0$ for all $i$, $j$ so that

    \[
      \frac{1}{s} \sum_{\tau = 1}^s E[y_i y_j] - p_i p_j \rightarrow 0
    \]

### 2. Digression: notes on first-order differential and difference equations

#### First-order, linear, constant coefficient differential equations

A first-order, linear, constant coefficient differential equation is an
equation of the form

\[
  a_1 y' + a_0 y = f(t)
\]

where $a_i$ are constants independent of $t$ and $f(t)$ is an inhomogenous
term (e.g., a "forcing function"). To solve this equation, we first find the
solution to the homogeneous equation

\[
  a_1 y' + a_0 y = 0
\]

and then use that solution as an integrating factor.

The solution to the homogeneous equation can be found by using an ansatz
solution of the form $y(t) = C e^{r t}$ where $C$ and $r$ are constants.
Plugging this into the differential equation yields a linear equation in $r$
(for higher-order differential equations, the same ansatz solution leads to
a polynomial equation in $r$):

\[
  a_1 r + a_0 = 0.
\]

Solving for $r$, we find that $r = -a_0 / a_1$ and that the solution to the
homogeneous equation is

\[
  C e^{r t} = C e^{-\left(\frac{a_0}{a_1}\right) t}
\]

To solve the inhomogeneous equation, we observe that

\[
  \frac{d}{dt} \left( e^{-rt} y \right)
  = e^{-rt} (y' -r y)
  = \left( \frac{1}{a_1} \right) e^{-rt} (a_1 y' - a_1 r y)
  = \left( \frac{1}{a_1} \right) e^{-rt} (a_1 y' + a_0 y)
\]

Therefore, we can transform the inhomogeneous equation into simple integration
problem by multiplying the equation by the _integrating factor_ $e^{-rt}$:

\[
  e^{-rt} (a_1 y' + a_0 y)
  = a_1 \frac{d}{dt} \left( e^{-rt} y \right)
  = e^{-rt} f(t)
\]

Integrating and multiplying through by $e^{rt} / a_1$, we obtain the solution

\[
  y(t) - y(0)
  = \frac{e^{rt}}{a_1} \int_0^t e^{-rs} f(s) ds
  = \frac{1}{a_1} \int_0^t e^{r(t - s)} f(s) ds
  = \frac{1}{a_1} \int_0^t e^{rs} f(t-s) ds ds
\]

#### First-order, linear, constant coefficient difference equations

A first-order, linear, constant coefficient difference (or recurrence) equation
is an equation of the form

\[
  a_1 y_{n+1} + a_0 y_{n} = f_n
\]

where $a_i$ are constants independent of $n$ and $f_n$ is an inhomogeneous
term. To draw the connection to differential equations, we define the
_difference operator_ $\Delta$ which can be defined by

\[
  \Delta y_{n} = y_{n} - y_{n-1}.
\]

Note that, unlike the differential operator, there are multiple conventions
that could be used to define $\Delta$. For instance, we could also define
$\Delta$ using a forward difference instead of a backward difference. The
different conventions yield slightly different equations (mainly in the way
that the coefficients are combined and with respect to indexing), but all
consistent conventions should lead to the same solutions.

Written in terms of the difference operator $\Delta$, the above recurrence
relation can be expressed as

\[
  a_1 \Delta y_{n+1} + (a_0 + a_1) y_{n} = f_n
\]

Defining new coefficients $b_0 = a_0 + a_1$ and $b_1 = a_1$, we arrive at the
discrete analog of the first-order, linear, constant coefficient differential
equation:

\[
  b_1 \Delta y_{n+1} + b_0 y_{n} = f_n.
\]

We can solve this equation using an approach analogous to the solution of the
differential equation, but we have to be a little more careful with keeping
track of indices.

To solve the homogeneous equation, we look for solutions of the form $C r^n$
and work with the original recurrence equation. Note that (1) looking for
solutions of the form $C e^{s n}$ and (2) using the form of the equation
involving the $\Delta$ operator yields completely equivalent results. It's just
easier and less tedious to work with the original recurrence equation and the
simpler ansatz. Plugging in our ansatz solution, we find that

\[
  a_1 r^{n+1} + a_0 r^{n} = 0,
\]

which implies that

\[
  a_1 r + a_0 = 0.
\]

Therefore, the solution to the homogeneous equation is

\[
  C \left(- \frac{a_0}{a_1}\right)^n
\]

To solve the inhomogeneous difference equation, it is convenient to use the
form of the equation involve the difference operator. Like the differential
equation case, we observe that we can multiply the left-hand side of the
equation by an appropriate _summation factor_ to transform the equation into
a simple summation problem.

Observe that

\[
  \Delta \left( r^{-(n+1)} y_{n+1} \right)
  = r^{-(n+1)} y_{n+1} - r^{-n} y_{n} \\
  =   r^{-(n+1)} y_{n+1}
    + (-r^{-(n+1)} y_{n} + r^{-(n+1)} y_{n})
    - r^{-n} y_{n} \\
  =   ( r^{-(n+1)} y_{n+1} - r^{-(n+1)} y_{n} )
    + r^{-(n+1)} y_{n} - r^{-n} y_{n} \\
  =   r^{-(n+1)} \Delta y_{n+1} + r^{-(n+1)} y_{n} - r^{-n} y_{n} \\
  =   r^{-(n+1)} \left( \Delta y_{n+1} + (1 - r) y_{n} \right ) \\
  =   r^{-(n+1)} \left( \frac{b_1 \Delta y_{n+1} + b_0 y_{n}}{b_1} \right )
\]

Multiplying the $\Delta$-form of the difference equation by the summation
factor, we transform the inhomogeneous difference equation into

\[
  r^{-(n+1)} \left( b_1 \Delta y_{n+1} + b_0 y_{n} \right )
  = b_1 \Delta \left( r^{-(n+1)} y_{n+1} \right)
  = r^{-(n+1)} f_n
\]

Summing and multiplying the result by $r^n / b_1$, we obtain the solution

\[
  y_n
  =   r^n y_0
    + \frac{r^n}{b_1} \sum_{i = 0}^{n-1} r^{-(i+1)} f_i
  =   r^n y_0
    + \frac{1}{b_1} \sum_{i = 0}^{n-1} r^{n-i-1} f_i
  =   r^n y_0
    + \frac{1}{b_1} \sum_{i = 0}^{n-1} r^{i} f_{n-i-1}
\]

#### Comments about differential/difference equations and their solutions

* __Long-time behavior of solutions of the homogeneous equation__

  * For the differential equation, when $a_1$ and $a_0$ have opposite sign, the
    solution of the homogeneous equation has an exponentially decaying
    solution.  This implies that the initial condition decay towards zero at
    long times.

  * For the difference equation, when $a_1$ and $a_0$ have opposite sign and
    $|a_0| < |a_1|$, the solution of the homogeneous equation has an
    exponentially decaying solution. This implies that the initial condition
    decay towards zero at long times.

* __Relation of inhomogenous solution to exponential moving averages__

  * The inhomogeneous part of the solution to an inhomogeneous difference
    equation has the form of an exponential moving average (exponential
    smoothing) of the inhomogeneous term. In the long-time limit, the
    exponential moving average approaches the expected value of the
    inhomogeneous term.

  * For differential equations, the inhomogeneous part of the solution to an
    inhomogeneous equation is the continuous analogue of an exponentially
    moving average.

* __Relation of equations to closed-loop (feedback) systems__

  * The dependence of the derivative (difference) on the current (recent)
    values of the solution indicates the presence of a feedback loop in the
    system modeled by the equations. It is this feedback that guarantees that
    transients will decay (for appropriate values of the coefficients).

    In general, closed-loop systems are more stable and operate more reliably
    than open-loop systems (i.e., no feedback).

### 3. Exercises / Open Questions

* Using an understanding of the behavior of first-order, linear, constant
  coefficient differential and difference equations, what are possible
  modifications that could be made to the Foldiak algorithm to improve its
  stability and/or reduce its sensitivity to parameters choices?

* Could Foldiak's algorithm be modified so that the bit probabilities arise
  naturally without having to be specified?

-------------------------------------------------------------------------------

[-----------------------------EXTERNAL LINKS-----------------------------]: #

[chrome-markdown-viewer]: https://chrome.google.com/webstore/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk
