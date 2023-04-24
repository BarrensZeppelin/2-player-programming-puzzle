#!/usr/bin/env pypy3

import base64
import os
import random
import shutil
import string
import subprocess
import tempfile
from pathlib import Path

task1 = base64.b64decode(
    b"""\
IyBDSEVDS1BPSU5UIDEKClRoZSBuZXh0IG9iamVjdGl2ZSBpcyB0byByZXRyaWV2ZSB0aGUgcGFz
c3BocmFzZSBmb3IgZGVjcnlwdGlvbjoKYG1jcnlwdCAtZCB0YXNrMi5tZC5uY2AKCkRlZmluZToK
JCQKIHhfMCA9IDAgXFwKIEEgPSA8QT4gXFwKIEIgPSA8Qj4gXFwKIEMgPSA8Qz4gXFwKIHhfaSA9
ICh4X3tpLTF9IFxjZG90IEEgKyBCKSBcbW9kIEMgXFwKIHlfaSA9IHhfaSBcbW9kIDI2CiQkCgpU
aGUgcGFzc3BocmFzZSBpcyB0aGUgY29uY2F0ZW5hdGlvbiBvZiB0aGUgbG93ZXJjYXNlIGxldHRl
cnMgY29ycmVzcG9uZGluZyB0byAkeV8xLCB5XzIsIFxsZG90cywgeV84JC4K
"""
).decode()
task2 = base64.b64decode(
    b"""\
IyBDSEVDS1BPSU5UIDIKCkxldCAkel9pID0geF9pIFxtb2QgMTAwMCQuCgokel8xLCB6XzIsIHpf
MywgXGxkb3RzLCB6X3sxMF40fSQgZ2VuZXJhdGUgYW4gdW5kaXJlY3RlZCBncmFwaCBvbiAxMDAw
IG5vZGVzLgoKRWFjaCBwYWlyCigkel8xJCBhbmQgJHpfMiQsICR6XzMkIGFuZCAkel80JCwgJHpf
NSQgYW5kICR6XzYkLCBldGMuKQpjb3JyZXNwb25kcyB0byBhbiBlZGdlLgoKVGhlIHBhc3NwaHJh
c2UgcmVxdWlyZWQgdG8gZGVjcnlwdCB0aGUgZmluYWwgdGFzayBpcyBhY3F1aXJlZCBieSBmaW5k
aW5nIHRoZQpub2RlcyBvbiB0aGUgdW5pcXVlIHNob3J0ZXN0IHBhdGggYmV0d2VlbiBub2RlcyA8
c3RhcnQ+IGFuZCA8ZW5kPiwgaW5jbHVzaXZlLgpUcmFuc2xhdGUgbm9kZSBpbmRpY2VzIHRvIGxv
d2VyY2FzZSBsZXR0ZXJzIGJ5IHRha2luZyB0aGUgaW5kaWNlcyBtb2R1bG8gMjYsCmFuZCBjb25j
YXRlbmF0ZSB0aGUgbGV0dGVycyBjb3JyZXNwb25kaW5nIHRvIHRoZSBub2RlcyBvbiB0aGUgcGF0
aC4K
"""
).decode()
task3 = base64.b64decode(
    b"""\
IyBDSEVDS1BPSU5UIDMKCllvdSB3aW4hCg==
"""
).decode()


def rand_number() -> int:
    """
    Generate a random number where the digits form at most two arithmetic
    progressions. It should make it possible to convey them to the keyboarder.
    """
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
# print(passwd2)

passwd1 = "".join(string.ascii_lowercase[v % 26] for v in X[1:9])

with tempfile.TemporaryDirectory(dir="") as pth:
    # Prepare final encrypted task
    task3_p = Path(pth) / "task3.md"
    task3_p.write_text(task3)
    subprocess.run(
        ["mcrypt", "--unlink", task3_p, "-k", passwd2], check=True, text=True
    )

    # Prepare task2
    task2_p = Path(pth) / "task2.md"
    task2_p.write_text(
        task2.replace("<start>", str(start_node)).replace("<end>", str(end_node))
    )
    subprocess.run(
        ["mcrypt", "--unlink", task2_p, "-k", passwd1], check=True, text=True
    )

    # Prepare task1
    task1_p = Path(pth) / "task1.md"
    task1_p.write_text(
        task1.replace("<A>", str(A)).replace("<B>", str(B)).replace("<C>", str(C))
    )

    subprocess.run(
        ["zip", "--quiet", "../puzzle.zip"] + [f.name for f in Path(pth).iterdir()],
        cwd=pth,
        check=True,
    )


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

    cnds = [p for p in dirs if p.count("/") == DIR_DEPTH - 1]
    assert cnds
    task_dir = task1 / random.choice(cnds)
    os.rename("puzzle.zip", task_dir / "task.zip")

    (root / "README.md").write_text(
        """\
# Welcome

Your first challenge is to _find_ the task description.

Your account has sudo privileges.
"""
    )

    subprocess.run(
        ["zip", "--quiet", "--recurse-paths", "../puzzle.zip", "task1", "README.md"],
        check=True,
        cwd=root,
    )
