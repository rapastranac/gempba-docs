# Background

GemPBA started as a research project during my MSc at Université de Sherbrooke, under the supervision of [Professor Manuel Lafond](https://www.usherbrooke.ca/informatique/nous-joindre/personnel/corps-professoral/professeurs/manuel-lafond). His work sits at the intersection of algorithm theory and bioinformatics: reconstructing evolutionary histories, solving gene reconciliation problems, and tackling NP-hard combinatorial questions that arise naturally when comparing genomes across species. Problems like weighted quartet consensus, phylogenetic network recognition, and maximum common contractions are all computationally hard, and branch-and-bound is one of the few practical approaches for finding exact solutions to them at meaningful scale.

My own focus was high-performance computing. Combining that with bioinformatics was not an obvious match at first glance, but it turned out that evolutionary biology is remarkably good at producing problems that no computer wants to solve. That made it a great fit. GemPBA is what came out of that overlap.

---

## What it is built for

Any algorithm that explores a search tree by branching on decisions and pruning dead ends can benefit from GemPBA. The framework handles the parallel infrastructure so you can focus on the algorithm itself.

Concrete problem domains where this applies:

- **Bioinformatics** — phylogenetic tree reconstruction, gene tree reconciliation, orthology prediction, and other combinatorial problems in comparative genomics
- **Graph problems** — maximum clique, minimum vertex cover, graph coloring, subgraph isomorphism
- **Routing and scheduling** — vehicle routing, job-shop scheduling, traveling salesman variants
- **Constraint satisfaction** — exact solvers for assignment and packing problems
- **Operations research** — integer programming subproblems solved via branch-and-bound

The common thread is a search space that is too large to enumerate naively but structured enough that pruning eliminates most of it. GemPBA distributes that search across threads and processes, with load balancing strategies designed for the unbalanced trees these problems produce in practice.

---

## The research

The framework was published in [Parallel Computing (2023)](https://doi.org/10.1016/j.parco.2023.103024) and the full design is described in my [MSc thesis](http://hdl.handle.net/11143/18687). The two main contributions, quasi-horizontal load balancing and the semi-centralized scheduler, are described in the [Why GemPBA](why-gempba.md) page.
