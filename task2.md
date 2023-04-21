# CHECKPOINT 2

Let $z_i = x_i \mod 1000$.

$z_1, z_2, z_3, \ldots, z_{10^4}$ generate an undirected graph on 1000 nodes.

Each pair
($z_1$ and $z_2$, $z_3$ and $z_4$, $z_5$ and $z_6$, etc.)
corresponds to an edge.

The passphrase required to decrypt the final task is acquired by finding the
nodes on the unique shortest path between nodes <start> and <end>, inclusive.
Translate node indices to lowercase letters by taking the indices modulo 26,
and concatenate the letters corresponding to the nodes on the path.
