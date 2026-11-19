# Differential form $\omega$
A differential $k$-form $\omega \in \Omega^k(M)$ on a manifold $M$ is a smooth assignment $p \longmapsto \omega_p$ at each point $p$ on the manifold, where $\omega_p$ is an alternating $k$-linear map
$$
\omega_p : \underbrace{T_p M \times \dots \times T_p M}_{k\text{ times}} \longrightarrow \mathbb{R}.
$$

- A $0$-form is just a function $p \longmapsto f(p)$.
- $1$-forms can be interpreted as covector fields
- in general $k$-forms correspond to alternating covariant tensors of rank $k$
- differential forms provide a coordinate independent geometrical framework

$\boxed{\Rightarrow\text{useful for physics in GR, EM}}$

**Visualization**: set of machines at each point on the manifold, that take $k$ vectors and spit out a number.
| differential form | manifold embedded in | interpretation |
| --- | --- | --- |
| $k$ | $k=n$ | number of dots inside an infinitesimal parallelpiped spanned by $k$-vectors |
| $1$ | $n\neq 1$ | number of crossings an infinitesimal vector has with an $(n-1)$-dimensional hyperplane |
| $k$ | $n>k$ | number of crossings a parallelpiped of vectors has with an $(n-k)$-dimensional hyperplane |

# Wedge product $\wedge$
The wedge product between a $k$-form $\alpha$ and an $\ell$-form $\beta$ can be defined pointwise by its action on vectors of the tangent space:
$$
(\alpha\wedge\beta)(v_1,\dots,v_{k+\ell}) = \frac{1}{k!\ell!} \sum_{\sigma\in S_{k+\ell}} \mathrm{sgn}(\sigma) \alpha(v_{\sigma(1)},\dots,v_{\sigma(k)}) \beta(v_{\sigma(k+1)},\dots,v_{\sigma(k+\ell)})
$$
the wedge product of the two differential forms is then itself a differential $(k+\ell)$-form.

When applied to a combination of a $1$-form $\alpha$ and a $k$-form $\beta$, the formula simplifies to
$$
(\alpha \wedge \beta)(v_0,\dots,v_k) = \sum_{i=0}^k (-1)^i \alpha(v_i) \beta(v_0,\dots,v_{i-1},v_{i+1},\dots,v_k).
$$

**Visualization**: The resulting differential form is the intersection of the hyperplanes of the product differential forms. Two $1$-forms $dx$ and $dy$ lead to a $2$-form $dx\wedge dy$, which is a bunch of lines in $z$-direction.

# Exterior derivative $d$
The exterior derivative is an operation
$$
d : \Omega^k(M) \longrightarrow \Omega^{k+1}(M)
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
The inner product of two $k$-forms $\alpha$ and $\beta$, that can be decomposed in $1$-forms $\alpha = \alpha_1\wedge\dots\wedge\alpha_k$ and $\beta=\beta_1\wedge\dots\wedge\beta_k$ is
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
\star: \Omega^k(M) \longrightarrow \Omega^{n-k}(M)
$$
which fulfills for all $k$-forms $\alpha,\beta$:
$$
\alpha \wedge \star \beta = \langle\alpha, \beta \rangle \mathrm{vol}_g
$$

## In the coframe picture
For a positively oriented orthonormal coframe $\theta^1,\dots,\theta^n$ the volume is given by
$$
\mathrm{vol}_g = \theta^1 \wedge \dots \wedge \theta^n.
$$
Applying the Hodge star operator to a basis $k$-form $\theta^{i_1}\wedge\dots\wedge\theta^{i_k}$ gives:
$$
\star (\theta^{i_1}\wedge\dots\wedge\theta^{i_k}) = \mathrm{sgn}(\sigma) \left(\prod_{r=1}^k \eta^{i_r i_r}\right) \theta^{j_1}\wedge\dots\wedge\theta^{j_{n-k}}
$$
Here $\sigma$ is the permutation $(i_1,\dots,i_k,j_1,\dots,j_{n-k})$.
It can be checked, that this fulfills the required condition.

## Properties
- $\star \star = (-1)^{k (n-k) + q}$ for a Lorentzian metric with $q$ negative directions
- $\alpha \wedge \star \alpha = \langle \alpha,\alpha\rangle\, \mathrm{vol}_g$

**Visualization**: TBD

# Generalized Stokes theorem
The generalized Stokes theorem states for a differential $(n-1)$-form on an $n$-dimensional manifold $M$
$$
\int_M d\omega = \int_{\partial M} \omega.
$$
To proof this, first consider a cube $C=[a,b]^n \sub \mathbb{R}^n$ and a differential $(n-1)$-form
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
\int_S d \omega = \iint_S \left( \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right) \mathrm{sgn}(n_z)\, dx dy + \iint_S \left( \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \right) \mathrm{sgn}(n_y)\,  dz dx + \iint_S \left( \frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z} \right) \mathrm{sgn}(n_x)\,  dy dz \\
= \iint_S \left( \nabla \times \bm{F} \right) \cdot \begin{pmatrix} \mathrm{sgn}(n_x)\, dy dz \\ \mathrm{sgn}(n_y)\, dz dx \\ \mathrm{sgn}(n_z)\,dx dy \end{pmatrix} \\
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
The integral of the $2$-form $\omega$ is given by:
$$
\int_{\partial V} \omega = \iint_{\partial V} F_x \mathrm{sgn}(n_x)\, dy dz + \iint_{\partial V} F_y \mathrm{sgn}(n_y)\, dz dx + \iint_{\partial V} F_z \mathrm{sgn}(n_z)\, dx dy \\
= \iint_{\partial V} \bm{F} \cdot d\bm{A}
$$

**Visualization**: TBD

# Poincaré lemma
The Poincaré lemma states that for a $(k+1)$-form $\beta$, with $d\beta = 0$ everywhere, there exists a $k$-form $\alpha$, such that $\beta = d\alpha$. This is true for a star-shaped region with respect to the origin.

To proof this take the following pointwise definition of $\alpha$:
$$
\alpha |_{x} (v_1, \dots, v_k) = \int_0^1 \beta|_{t x}(x,t v_1,\dots,t v_k) dt
$$
The goal is to show $d \alpha |_{x} (v_0, \dots, v_k) = \beta|_{x}(v_0, \dots, v_k)$. First compute the exterior derivative of $\alpha$. In a chart we may take the $v_i$ to be constant, leading to
$$
d\alpha |_{x} (v_0, \dots, v_k) = \sum_{i=0}^{k} (-1)^i \partial_{v_i} (\alpha|_x (v_0,\dots,v_{i-1},v_{i+1},\dots,v_k)).
$$

Now insert the definition of $\alpha$ and differentiate under the integral:
$$
d\alpha |_{x} (v_0, \dots, v_k)
= \sum_{i=0}^{k} (-1)^i \int_0^1 t^k \left[ t (\partial_{v_i}\beta)\big|_{tx}(x,v_0,\dots,v_{i-1},v_{i+1},\dots,v_k)
+ \beta\big|_{tx}(v_i,v_0,\dots,v_{i-1},v_{i+1},\dots,v_k) \right] dt.
$$

The second term can be evaluated and simplified by moving the vector $v_i$ $i$-times right, which comes with a factor $(-1)^i$ and integrating $t^k$:
$$
\sum_{i=0}^{k} (-1)^i \int_0^1 t^k \beta\big|_{tx}(v_i,v_0,\dots,v_{i-1},v_{i+1},\dots,v_k) dt = (k+1) \int_0^1 t^k \beta|_{tx}(v_0, \dots, v_k) dt
$$

The first term can be rewritten using the identity
$$
d\beta|_{p}(x,v_0,\dots,v_k) = (\partial_x \beta)|_{p}(v_0,\dots,v_k) - \sum_{i=0}^k (-1)^i (\partial_{v_i}\beta)|_{p}(x,v_0,\dots,v_{i-1},v_{i+1},\dots,v_k).
$$
Together with the assumption $d\beta = 0$ this gives:
$$
\sum_{i=0}^{k} (-1)^i \int_0^1 t^{k+1} (\partial_{v_i}\beta)\big|_{tx}(x,v_0,\dots,v_{i-1},v_{i+1},\dots,v_k)\, dt\\
= \int_0^1 t^{k+1} (\partial_x \beta)|_{tx}(v_0,\dots,v_k)\, dt
$$

The exterior derivative of $\alpha$ can therefore be written as
$$
d\alpha |_{x} (v_0, \dots, v_k) = \int_0^1 \frac{d}{dt}\left(t^{k+1} \beta|_{tx}(v_0,\dots,v_k)\right) dt \\
= \beta|_{x}(v_0,\dots,v_k),
$$
completing the proof.

**Visualization**: TBD

# Cartan structure equations (coordinate derivation)

Let $e_a$ be a local frame, $e^a$ its dual coframe, and define the connection $1$-forms by
$$
\nabla_Xe_b=\omega^a{}_b(X)e_a.
$$

The components are $e^a{}_\mu=e^a(\partial_\mu)$, $\omega_\mu{}^a{}_b=\omega^a{}_b(\partial_\mu)$.

## Lie bracket
For vector fields $X=X^\rho\partial_\rho$, $Y=Y^\rho\partial_\rho$.
The Lie bracket has components
$$
[X,Y]^\rho = X^\sigma\partial_\sigma Y^\rho - Y^\sigma\partial_\sigma X^\rho.
$$
For $X=\partial_\mu$ and $Y=\partial_\nu$,
$$
X^\rho=\delta^\rho_\mu, \qquad Y^\rho=\delta^\rho_\nu.
$$
These components are constant, so
$$
[\partial_\mu,\partial_\nu]=0.
$$

## First structure equation
The torsion is defined by
$$
T(X,Y)=\nabla_XY-\nabla_YX-[X,Y].
$$
Its frame components are the $2$-forms
$$
T^a(X,Y)=e^a(T(X,Y)).
$$
Since $\partial_\nu=e^b{}_\nu e_b$, we have
$$
\begin{aligned}
\nabla_{\partial_\mu}\partial_\nu &= \nabla_{\partial_\mu}(e^b{}_\nu e_b)\\
&= (\partial_\mu e^b{}_\nu)e_b + e^b{}_\nu\nabla_{\partial_\mu}e_b\\
&= (\partial_\mu e^a{}_\nu)e_a + e^b{}_\nu\omega^a{}_{b\mu}e_a.
\end{aligned}
$$
Therefore,
$$
e^a(\nabla_{\partial_\mu}\partial_\nu) = \partial_\mu e^a{}_\nu + \omega^a{}_{b\mu}e^b{}_\nu.
$$
Using $[\partial_\mu,\partial_\nu]=0$,
$$
\begin{aligned}
T^a(\partial_\mu,\partial_\nu) &= e^a\left( \nabla_{\partial_\mu}\partial_\nu - \nabla_{\partial_\nu}\partial_\mu \right)\\
&= \partial_\mu e^a{}_\nu-\partial_\nu e^a{}_\mu + \omega^a{}_{b\mu}e^b{}_\nu - \omega^a{}_{b\nu}e^b{}_\mu.
\end{aligned}
$$
But
$$
de^a(\partial_\mu,\partial_\nu) = \partial_\mu e^a{}_\nu-\partial_\nu e^a{}_\mu
$$
and
$$
(\omega^a{}_b\wedge e^b)(\partial_\mu,\partial_\nu) = \omega^a{}_{b\mu}e^b{}_\nu - \omega^a{}_{b\nu}e^b{}_\mu.
$$
Hence
$$
T^a=de^a+\omega^a{}_b\wedge e^b.
$$

# Second structure equation
The curvature is defined by
$$
R(X,Y)Z = \nabla_X\nabla_YZ - \nabla_Y\nabla_XZ - \nabla_{[X,Y]}Z.
$$
The curvature $2$-forms are defined by
$$
R(X,Y)e_b=R^a{}_b(X,Y)e_a.
$$
Now
$$
\nabla_{\partial_\nu}e_b = \omega^c{}_{b\nu}e_c.
$$
Therefore,
$$
\begin{aligned}
\nabla_{\partial_\mu}\nabla_{\partial_\nu}e_b &= \nabla_{\partial_\mu} \left(\omega^c{}_{b\nu}e_c\right)\\
&= (\partial_\mu\omega^c{}_{b\nu})e_c + \omega^c{}_{b\nu}\nabla_{\partial_\mu}e_c\\
&= \left( \partial_\mu\omega^a{}_{b\nu} + \omega^a{}_{c\mu}\omega^c{}_{b\nu} \right)e_a.
\end{aligned}
$$
Interchanging $\mu$ and $\nu$,
$$
\nabla_{\partial_\nu}\nabla_{\partial_\mu}e_b = \left( \partial_\nu\omega^a{}_{b\mu} + \omega^a{}_{c\nu}\omega^c{}_{b\mu} \right)e_a.
$$
Since $[\partial_\mu,\partial_\nu]=0$,
$$
\begin{aligned}
R^a{}_b(\partial_\mu,\partial_\nu) &= \partial_\mu\omega^a{}_{b\nu} - \partial_\nu\omega^a{}_{b\mu}\\
&+ \omega^a{}_{c\mu}\omega^c{}_{b\nu} - \omega^a{}_{c\nu}\omega^c{}_{b\mu}.
\end{aligned}
$$
But
$$
d\omega^a{}_b(\partial_\mu,\partial_\nu) = \partial_\mu\omega^a{}_{b\nu} - \partial_\nu\omega^a{}_{b\mu}
$$
and
$$
(\omega^a{}_c\wedge\omega^c{}_b)(\partial_\mu,\partial_\nu) = \omega^a{}_{c\mu}\omega^c{}_{b\nu} - \omega^a{}_{c\nu}\omega^c{}_{b\mu}.
$$
Therefore,
$$
R^a{}_b = d\omega^a{}_b + \omega^a{}_c\wedge\omega^c{}_b.
$$

# Cartan structure equations (coordinate free / differential forms)
Let $e_a$ be a local frame, $e^a$ its dual coframe, and define the connection $1$-forms by
$$
\nabla_Xe_b=\omega^a{}_b(X)e_a.
$$

## First structure equation
The torsion is
$$
T(X,Y)=\nabla_XY-\nabla_YX-[X,Y].
$$
Define its coframe components by
$$
T^a(X,Y)=e^a(T(X,Y)).
$$
Write $Y=e^b(Y)e_b$. Then
$$
\begin{aligned}
\nabla_XY &= \nabla_X \big(e^b(Y)e_b\big)\\
&= \nabla_X \big( e^b(Y) \big) e_b + e^b(Y) \nabla_X e_b.
\end{aligned}
$$
Therefore,
$$
e^a(\nabla_XY) = \nabla_X \big(e^a(Y)\big) + \omega^a{}_b(X)e^b(Y).
$$
Substituting into the torsion definition,
$$
\begin{aligned}
T^a(X,Y) &= \nabla_X \big(e^a(Y)\big) -\nabla_Y \big(e^a(X)\big) - e^a([X,Y])\\
&+ \omega^a{}_b(X)e^b(Y) - \omega^a{}_b(Y)e^b(X).
\end{aligned}
$$
The first line is
$$
de^a(X,Y) = \nabla_X (e^a(Y))-\nabla_Y (e^a(X))-e^a([X,Y]),
$$
and the second is
$$
(\omega^a{}_b\wedge e^b)(X,Y) = \omega^a{}_b(X)e^b(Y) - \omega^a{}_b(Y)e^b(X).
$$
Hence, for all $X,Y$,
$$
T^a(X,Y) = \big(de^a+\omega^a{}_b\wedge e^b\big)(X,Y).
$$
Therefore,
$$
T^a=de^a+\omega^a{}_b\wedge e^b.
$$

## Second structure equation
The curvature is
$$
R(X,Y)Z = \nabla_X\nabla_YZ - \nabla_Y\nabla_XZ - \nabla_{[X,Y]}Z.
$$
Define the curvature $2$-forms by
$$
R(X,Y)e_b=R^a{}_b(X,Y)e_a.
$$
Using $\nabla_Ye_b=\omega^c{}_b(Y)e_c$, we obtain
$$
\begin{aligned}
\nabla_X \nabla_Y e_b &= \nabla_X \big( \omega^c{}_b(Y) e_c \big)\\
&= \nabla_X \big(\omega^c{}_b(Y)\big) e_c + \omega^c{}_b(Y) \nabla_X e_c\\
&= \left[ \nabla_X \big(\omega^a{}_b(Y)\big) + \omega^a{}_c(X) \omega^c{}_b(Y) \right]e_a.
\end{aligned}
$$
Likewise,
$$
\nabla_Y \nabla_X e_b = \left[ \nabla_Y \big(\omega^a{}_b(X)\big) + \omega^a{}_c(Y) \omega^c{}_b(X) \right]e_a,
$$
and
$$
\nabla_{[X,Y]}e_b = \omega^a{}_b([X,Y])e_a.
$$
Thus
$$
\begin{aligned}
R^a{}_b(X,Y) &= \nabla_X \big(\omega^a{}_b(Y)\big) - \nabla_Y \big(\omega^a{}_b(X)\big) - \omega^a{}_b([X,Y])\\
&+ \omega^a{}_c(X)\omega^c{}_b(Y) - \omega^a{}_c(Y)\omega^c{}_b(X).
\end{aligned}
$$
The first line is
$$
d\omega^a{}_b(X,Y),
$$
and the second is
$$
(\omega^a{}_c \wedge \omega^c{}_b)(X,Y).
$$
Therefore,
$$
R^a{}_b = d\omega^a{}_b + \omega^a{}_c\wedge\omega^c{}_b.
$$

In matrix notation, the two equations are simply
$$
\boxed{T=de+\omega\wedge e},
\qquad
\boxed{R=d\omega+\omega\wedge\omega}.
$$

# Applications
- [de Rham cohomology]
- Maxwell equations
- Cartan structure equations
- Einstein equations via forms