# Differential form $\omega$
A differential $k$-form $\omega \in \Omega^k(M)$ on a manifold $M$ is a smooth assignment $p \longmapsto \omega_p$ at each point $p$ on the manifold, where $\omega_p$ is an alternating $k$-linear map
$$
\omega_p : \underbrace{T_p M \times \dots \times T_p M}_{k\text{ times}} \longmapsto \mathbb{R}.
$$

- A $0$-form is just a function $p \longmapsto f(p)$.
- $1$-forms can be interpreted as covectorfields
- in general $k$-forms correspond to alternating covariant tensors of rank $k$
- differential forms provide a coordinate independent geometrical framework

$\boxed{\Rightarrow\text{useful for physics in GR, EM}}$

**Interpretation**: set of machines at each point on the manifold, that take $k$ vectors and spit out a number. (Interpretation as integrands over curves, surfaces, volumes (manifolds) later)

# Wedge product $\wedge$
The wedge product between a $k$-form $\alpha$ and an $\ell$-form $\beta$ can be defined pointwise by it's action on vectors of the tangent space:
$$
(\alpha\wedge\beta)(v_1,\dots,v_{k+\ell}) = \frac{1}{k!\ell!} \sum_{\sigma\in S_{k+\ell}} \mathrm{sgn}(\sigma) \alpha(v_{\sigma(1)},\dots,v_{\sigma(k)}) \beta(v_{\sigma(k+1)},\dots,v_{\sigma(k+\ell)})
$$
the wedge product of the two differential forms is then itself a differential $(k+\ell)$-form.

**Interpretation**: TBD

# Exterior derivative $d$
The exterior derivative is an operation
$$
d : \Omega^k(M) \longmapsto \Omega^{k+1}(M)
$$
and generalizes gradient, curl and divergence.

For a $0$-form $f$ the exterior derivative is defined to be the differential $df$, which acting on a vectorfield $v$ becomes the directional derivative of $f$ along $v$
$$
df(v) = v f = v^i \partial_i f.
$$
Importantly this quantity is coordinate independent (though one may write it out explicitly in a coordinate basis for concrete calculations).

## Definition in coordinates
Any $k$-form can be written in a coordinate basis as
$$
\omega = \sum_{i_1 < \dots < i_k} f_{i_1 \dots i_k} dx^{i_1} \wedge \dots \wedge dx^{i_k}.
$$

The exterior derivative is then defined to be
$$
d\omega = \sum_{i_1 < \dots < i_k} df_{i_1 \dots i_k} \wedge dx^{i_1} \wedge \dots \wedge dx^{i_k},
$$
with $df_{i_1 \dots i_k} = (\partial_j f_{i_1 \dots i_k})\, dx^j$.

From this definition one can derive the
- graded Leibniz rule: $d (\alpha \wedge \beta) = d\alpha \wedge \beta + (-1)^k \alpha \wedge d\beta$ for a $k$-form $\alpha$
- nilpotence: $d^2 = 0$

**Interpretation**: TBD

# Inner product
The inner product of two $k$-forms $\alpha$ and $\beta$, that can be decomposed in $1$-forms $\alpha_1,\dots,\alpha_k$ and $\beta_1,\dots,\beta_k$ is
$$
\langle \alpha, \beta \rangle = \langle \alpha_1\wedge\cdots\wedge\alpha_k,\,
\beta_1\wedge\cdots\wedge\beta_k\rangle
=
\det
\begin{pmatrix}
\langle \alpha_1,\beta_1\rangle & \cdots & \langle \alpha_1,\beta_k\rangle\\
\vdots & & \vdots\\
\langle \alpha_k,\beta_1\rangle & \cdots & \langle \alpha_k,\beta_k\rangle
\end{pmatrix}.
$$
This can be extended to general $k$-forms by bilinearity.
Here the standard inner product of two one forms $v=v_\mu dx^\mu, w=w_\mu dx^\mu$ is induced by the inverse metric
$$
\langle v, w \rangle = g^{\mu \nu} v_\mu w_\nu.
$$
The inverse metric components can be obtained from the metric, which is defined via an orthonormal coframe $\theta^1,\dots,\theta^n$ as
$$
\quad g = \eta_{ab} \theta^a \otimes \theta^b.
$$
The orthonormal coframe fulfills
$$
\langle \theta^i, \theta^j \rangle = \eta^{ij}
$$
If one expresses the $k$-forms $\alpha = \sum_I a_I \theta^I $ and $\beta = \sum_J b_J \theta^J$ in the $k$-form basis given by the wedge products $\theta^I = \theta^{i_1}\wedge\dots\wedge\theta^{i_k}$ of the orthonormal coframe, the inner product can be written as
$$
\langle \alpha, \beta \rangle = \sum_{I,J} a_I b_J \langle \theta^I, \theta^J \rangle.
$$
With the inner product of the coframes
$$
\langle \theta^I,\theta^J\rangle
=
\det\bigl(\eta^{i_r j_s}\bigr)_{1\le r,s\le k}
=
\begin{cases}
\displaystyle \prod_{r=1}^k \eta^{i_r i_r}, & I=J,\\[1ex]
0, & I\neq J.
\end{cases}
$$

**Interpretation**: TBD

# Hodge star $\star$
The Hodge star is the unique linear map
$$
\star: \Omega^k(M) \longmapsto \Omega^{n-k}(M)
$$
which fulfills for all $k$-forms $\alpha,\beta$:
$$
\alpha \wedge \star \beta = \langle\alpha, \beta \rangle \mathrm{vol}_g
$$

## In the coframe picture
For an oriented coframe $\theta^1,\dots,\theta^n$ the volume is given by
$$
\mathrm{vol}_g = \theta^1 \wedge \dots \wedge \theta^n.
$$
Applying the Hodge star operator to a basis $k$-frame $\theta^{i_1}\wedge\dots\wedge\theta^{i_k}$ gives:
$$
\star (\theta^{i_1}\wedge\dots\wedge\theta^{i_k}) = \mathrm{sgn}(\sigma) \theta^{j_1}\wedge\dots\wedge\theta^{j_{n-k}}
$$
Here $\sigma$ is the permutation $(i_1,\dots,i_k,j_1,\dots,j_{n-k})$.
It can be checked, that this fulfills the required condition.

## Properties
- $\star \star = (-1)^{k (n-k)}$
- $\alpha \wedge \star \alpha = \|\alpha\|^2 \mathrm{vol}_g$

**Interpretation**: TBD

# Applications
- Generalized Stokes theorem
- de Rham cohomology and the Poincaré lemma
- Maxwell equations
- Cartan structure equations
- Einstein equations via forms