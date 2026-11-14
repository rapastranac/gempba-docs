# Why GemPBA

If you have ever tried to parallelize a branch-and-bound algorithm by hand, you already know the pain. You start with a clean recursive function, it works great, and then someone says "can we use all these CPU cores?" Suddenly you are drowning in thread pools, work queues, mutexes protecting a shared best-solution, and recursive calls that somehow need to coordinate across threads without stomping on each other.

GemPBA was built because the same problem kept appearing from scratch for every new branching algorithm. The scheduling scaffold was always the same; only the algorithm in the middle changed. And every time an existing library appeared as a candidate, either no one could figure out how to build it (the documentation was three paragraphs and a "see the tests"), or it was so tightly coupled to one algorithm structure that adapting it meant basically rewriting it.

GemPBA's answer to this is a framework that inserts itself into your recursion through a small set of parameter additions. You keep writing your algorithm the way you always have. GemPBA handles the rest.

Distributed, it also gets a hard part right that hand-rolled schedulers usually guess at: knowing when the search is over. GemPBA's MPI schedulers detect termination exactly, with **Dijkstra–Scholten** acknowledgements rather than a timeout, so a run never ends with work still in flight and never idles waiting out a quiet period ([How the run ends](scheduler-topologies.md#how-the-run-ends)). And when you need it to end sooner, a stop winds it down gracefully, and the run tells you whether its result is proven or the best found so far ([Stopping a Run](stopping-a-run.md)).
