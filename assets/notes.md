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

**Visualization**: set of machines at each point on the manifold, that take $k$ vectors and spit out a number. (Interpretation as integrands over curves, surfaces, volumes (manifolds) later)

# Wedge product $\wedge$
The wedge product between a $k$-form $\alpha$ and an $\ell$-form $\beta$ can be defined pointwise by it's action on vectors of the tangent space:
$$
(\alpha\wedge\beta)(v_1,\dots,v_{k+\ell}) = \frac{1}{k!\ell!} \sum_{\sigma\in S_{k+\ell}} \mathrm{sgn}(\sigma) \alpha(v_{\sigma(1)},\dots,v_{\sigma(k)}) \beta(v_{\sigma(k+1)},\dots,v_{\sigma(k+\ell)})
$$
the wedge product of the two differential forms is then itself a differential $(k+\ell)$-form.

**Visualization**: TBD

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

**Visualization**: TBD

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

**Visualization**: TBD

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

**Visualization**: TBD

# Generalized Stokes theorem
The generalized Stokes theorem states for a differential $(n-1)$-form on an $n$-dimensional manifold $M$
$$
\int_M d\omega = \int_{\partial M} \omega.
$$
To proof this, first consider a cube $C=[a,b]^n \sub \mathbb{R}$ and a differential $(n-1)$-form
$$
\omega = \sum_{i=1}^n (-1)^{i-1} f_i(x) dx^1 \wedge \dots \wedge dx^{i-1} \wedge dx^{i+1} \wedge \dots \wedge dx^n.
$$
The exterior derivative of this differential form is then
$$
d \omega = \sum_{i=1}^n (-1)^{i-1} df_i(x) \wedge dx^1 \wedge \dots \wedge dx^{i-1} \wedge dx^{i+1} \wedge \dots \wedge dx^n \\
= \sum_{i=1}^n (-1)^{i-1} \sum_{j=1}^n (\partial_j f_i) dx^j \wedge dx^1 \wedge \dots \wedge dx^{i-1} \wedge dx^{i+1} \wedge \dots \wedge dx^n \\
= \sum_{i=1}^n (-1)^{i-1} (\partial_i f_i) dx^i \wedge dx^1 \wedge \dots \wedge dx^{i-1} \wedge dx^{i+1} \wedge \dots \wedge dx^n \\
= \sum_{i=1}^n (\partial_i f_i) dx^1 \wedge \dots \wedge dx^n
$$
With this we obtain for the cube
$$
\int_C d\omega = \sum_{i=1}^n \int_C (\partial_i f_i) dx^1 \dots dx^n \\
= \sum_{i=1}^n \int_? (f_i(x^i=b) - f_i(x^i=a)) dx^1 \dots dx^{i-1} dx^{i+1} \dots dx^n \\
= \int_{\partial C} \sum_{i=1}^n (-1)^{i-1} f_i(x) dx^1 \wedge \dots \wedge dx^{i-1} \wedge dx^{i+1} \wedge \dots \wedge dx^n \\
= \int_{\partial C} \omega
$$
For any cube we have $\int_C d\omega = \int_{\partial C} \omega$. By decomposing our desired region of integration $M$ into a lot of small cubes we can then apply the theorem to each cube.
The faces of the cubes inside the region will have two contributions each with opposite orientation, leading to opposite sign. They therefore cancel out, leaving only the boundary terms.

| Theorem | $M$ | $\omega$ | $d\omega$ | Equation |
|---|---|---|---|---|
| Generalized Stokes | oriented $(k+1)$-manifold with boundary | $k$-form | exterior derivative | $\displaystyle \int_M d\omega=\int_{\partial M}\omega$ |
| Fundamental theorem of calculus | $[a,b]$ | $f$ | $f'(x)\,dx$ | $\displaystyle \int_a^b f'(x)\,dx=f(b)-f(a)$ |
| Gradient theorem | oriented curve $\gamma$ from $a$ to $b$ | $f$ | $df$ | $\displaystyle \int_\gamma \nabla f\cdot d\bm r=f(b)-f(a)$ |
| Green’s theorem | plane region $D$ | $P\,dx+Q\,dy$ | $(\partial_x Q- \partial_y P)\,dx\wedge dy$ | $\displaystyle \iint_D (\partial_x Q-\partial_y P)\,dA=\oint_{\partial D}P\,dx+Q\,dy$ |
| Stokes theorem | oriented surface $S$ | $F_x\,dx+F_y\,dy+F_z\,dz$ | $(\nabla\times\bm F)\cdot d\bm{A}$ | $\displaystyle \iint_S(\nabla\times\bm F)\cdot d\bm{A}=\oint_{\partial S}\bm F\cdot d\bm r$ |
| Gauss theorem | volume $V$ | $F_x\,dy\wedge dz+F_y\,dz\wedge dx+F_z\,dx\wedge dy$ | $(\nabla\cdot\bm F)\,dV$ | $\displaystyle \iiint_V(\nabla\cdot\bm F)\,dV=\iint_{\partial V}\bm F\cdot d\bm{A}$ |

## Stokes theorem
Compute the exterior derivative of the differential $1$-form:
$$
d\omega = \left( \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right) dx \wedge dy + \left( \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \right) dz \wedge dx + \left( \frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z} \right) dy \wedge dz
$$
Integration over the exterior derivative gives
$$
\int_S d \omega = \iint_S \left( \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right) n_z\, dx dy + \iint_S \left( \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \right) n_y\,  dz dx + \iint_S \left( \frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z} \right) n_x\,  dy dz \\
= \iint_S \left( \nabla \times \bm{F} \right) \cdot \begin{pmatrix} n_x\, dy dz \\ n_y\, dz dx \\ n_z\,dx dy \end{pmatrix} \\
=  \iint_S \left( \nabla \times \bm{F} \right) \cdot d\bm{A}.
$$

## Gauß theorem
The exterior derivative of the $2$-form is
$$
d\omega = \left( \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z} \right)dx \wedge dy \wedge dz.
$$
It is easy to see that the integral becomes:
$$
\int_V d\omega = \iiint_V (\nabla\cdot\bm F)\,dV
$$
The integral of the $1$-form $\omega$ is given by:
$$
\int_{\partial V} \omega = \iint_{\partial V} F_x n_x\, dy dz + \iint_{\partial V} F_y n_y\, dz dx + \iint_{\partial V} F_z n_z\, dx dy \\
= \iint_{\partial V} \bm{F} \cdot d\bm{A}
$$

**Visualization**: TBD

# Poincaré lemma
The Poincaré lemma states that for a $(k+1)$-form $\beta$, with $d\beta = 0$ everywhere, there exists a $k$-form $\alpha$, such that $\beta = d\alpha$.

To proof this take the following pointwise definition of $\alpha$:
$$
\alpha |_{\bm{x}} (\bm{v}_1, \dots, \bm{v}_k) = \int_0^1 \beta|_{t\bm{x}}(\bm{x},t\bm{v}_1,\dots,t\bm{v}_k) dt
$$

The goal is to show $d \alpha |_{\bm{x}} (\bm{v}_0, \dots, \bm{v}_k) = \beta|_{\bm{x}}(\bm{v}_0, \dots, \bm{v}_k)$. First compute the exterior derivative of $\alpha$:
$$
d\alpha |_{\bm{x}} (\bm{v}_0, \dots, \bm{v}_k) =
$$

# Applications
- de Rham cohomology and the Poincaré lemma
- Maxwell equations
- Cartan structure equations
- Einstein equations via forms