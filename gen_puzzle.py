#!/usr/bin/env pypy3

import os
import random
import shutil
import string
import subprocess
import tempfile
from pathlib import Path


def rand_number() -> int:
    while True:
        n = random.randint(10**5, 10**6) * 2 + 1
        s = list(map(int, str(n)))
        prog = [y - x for x, y in zip(s, s[1:])]
        if sum(x != y for x, y in zip(prog, prog[1:])) > 1:
            continue
        return n


N = 10**3
while True:
    A, B, C = (rand_number() for _ in range(3))
    X = [0]
    for i in range(10**4):
        X.append((X[-1] * A + B) % C)

    adj = [[] for _ in range(N)]
    for x, y in zip(X[1::2], X[2::2]):
        x %= N
        y %= N
        adj[x].append(y)
        adj[y].append(x)

    assert sum(len(l) for l in adj) == len(X) - 1

    for start_node in range(N):
        D = [-1] * N
        prev = [-1] * N
        bad = [False] * N
        D[start_node] = 0
        Q = [start_node]

        for i in Q:
            d = D[i]
            for j in adj[i]:
                bad[j] |= bad[i]
                if D[j] == -1:
                    prev[j] = i
                    D[j] = d + 1
                    Q.append(j)
                elif D[j] == d + 1:
                    # print(adj[i], j)
                    bad[j] = True

        cands = [i for i in range(N) if 5 <= D[i] <= 10 and not bad[i]]
        if cands:
            end_node = cands.pop()
            break
    else:
        continue

    break

    # print("NO", C, sum(bad), sorted(D)[-10:])

path = [end_node]
while path[-1] != start_node:
    path.append(prev[path[-1]])

print(A, B, C, start_node, end_node)
passwd2 = "".join(string.ascii_lowercase[v % 26] for v in reversed(path))
print(passwd2)

passwd1 = "".join(string.ascii_lowercase[v % 26] for v in X[1:9])

with tempfile.TemporaryDirectory(dir="") as pth:
    # Prepare final encrypted task
    task3 = Path(pth) / "task3.md"
    shutil.copy("task3.md", task3)
    subprocess.run(["mcrypt", "--unlink", task3, "-k", passwd2], check=True, text=True)

    # Prepare task2
    task2 = Path(pth) / "task2.md"
    shutil.copy("task2.md", task2)
    subprocess.run(["mcrypt", "--unlink", task2, "-k", passwd1], check=True, text=True)

    # Prepare task1
    task1 = Path(pth) / "task1.md"
    task1.write_text(
        Path("task1.md")
        .read_text()
        .replace("<A>", str(A))
        .replace("<B>", str(B))
        .replace("<C>", str(C))
    )

    subprocess.run(["zip", "../puzzle.zip"] + [f.name for f in Path(pth).iterdir()], cwd=pth, check=True)

exit()


DIR_DEPTH = 7
DIR_SIZE = 10**4

with tempfile.TemporaryDirectory(dir="") as pth:
    root = Path(pth).absolute()

    task1 = root / "task1"
    task1.mkdir()

    dirs = []
    for _ in range(DIR_SIZE):
        pth = "/".join(
            "".join(random.choices(string.ascii_letters, k=random.randint(1, 4)))
            for _ in range(random.randint(1, DIR_DEPTH))
        )
        dirs.append(pth)

    dirs.sort()

    for pth in dirs:
        (task1 / pth).mkdir(parents=True, exist_ok=True)

    cands = [p for p in dirs if p.count("/") == DIR_DEPTH - 1]
    assert cands
    task_dir = task1 / random.choice(cands)
