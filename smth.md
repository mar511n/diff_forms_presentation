## IV. Further relations for a dislocation 

### 1. Relation between displacement and Burgers vector

The displacement field $u^i$ ist multivalued while the distorsion $du^i$ is continuous.

Then, $d^2 u^i = \text{rot grad } u^i$ does not vanish for multivalued $u^i$ (!).

Inserted into the torsion integrated over a surface element yields the Burgers vector
$$ b^i = \int\int T^i = \int\int d\theta^i = \int\int \text{rot grad }u^i dx \wedge dy = \oint \text{grad }u^i dl = \oint du^i = \Delta u^i$$

### 2. Relation between the conformal factor $\phi$ and the Burgers vector

Bringing the metric to the isothermal diagonal form

$$ g_{ij} = \begin{pmatrix} \phi & 0 \\ 0 & \phi \end{pmatrix} $$

with coframes

$$ \theta^a = \phi dx^a $$

such that 

$$ g = \delta_{ab} \theta^a \theta^b = \phi^2 (dx^2 + dy^2) $$

and declaring it parallel $\omega^a{}_b = 0$ gives the torsion

$$ T^a = d\theta^a = d\phi \wedge dx^a = \partial_b \phi dx^b \wedge dx^a = -\epsilon^{ab} \partial_b \phi dx \wedge dy$$

The Burgers vector is obtained via integration (averaging) $b^a = \int\int T^a$ and requires an invariant(?) area element $dA = \sqrt{\deg g} x^1 \wedge dx^2$ with $\sqrt{\det g} = \phi$. Therefore, we rewrite
$ T^a = -\epsilon^{ab} \partial_b \log \phi dA$
so that
$$ b^a = -\epsilon^{ab} \partial_b \log \phi$$