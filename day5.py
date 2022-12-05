from typing import NamedTuple

class Instr(NamedTuple):
  num: int
  src: int
  dest: int

def rearrange1(stacks: list[list[str]], instr: list[Instr]):
  for (num, src, dest) in instr:
    for _ in range(num):
      stacks[dest - 1].append(stacks[src - 1].pop())
  return stacks

def rearrange2(stacks: list[list[str]], instr: list[Instr]):
  for (num, src, dest) in instr:
    stacks[dest - 1].extend(stacks[src - 1][-num:])
    stacks[src - 1] = stacks[src - 1][:-num]
  return stacks

def solve(stacks_in: str, instr_in: str):
  stacks_in_lines = stacks_in.strip('\n').splitlines()
  stacks: list[list[str]] = \
    [[] for _ in range((len(stacks_in_lines[0]) + 1) // 4)]
  for line in stacks_in_lines:
    for i, stack in enumerate(stacks):
      if line[1 + i * 4] != ' ':
        stack.append(line[1 + i * 4])
  for stack in stacks:
    stack.reverse()
  instr = [
    Instr(*[int(x) for x in line.split()[1::2]])
    for line in instr_in.strip().splitlines()
  ]
  print(*[
    ''.join([
      stack[-1] for stack in rerrange([
        stack.copy() for stack in stacks
      ], instr)
    ])
    for rerrange in [rearrange1, rearrange2]
  ])

solve("""
    [D]    
[N] [C]    
[Z] [M] [P]
""", """
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""")

solve("""
[D]                     [N] [F]    
[H] [F]             [L] [J] [H]    
[R] [H]             [F] [V] [G] [H]
[Z] [Q]         [Z] [W] [L] [J] [B]
[S] [W] [H]     [B] [H] [D] [C] [M]
[P] [R] [S] [G] [J] [J] [W] [Z] [V]
[W] [B] [V] [F] [G] [T] [T] [T] [P]
[Q] [V] [C] [H] [P] [Q] [Z] [D] [W]
""", """
move 1 from 3 to 9
move 2 from 2 to 1
move 3 from 5 to 4
move 1 from 1 to 8
move 1 from 3 to 9
move 1 from 5 to 7
move 1 from 5 to 3
move 4 from 4 to 2
move 2 from 3 to 4
move 1 from 3 to 2
move 6 from 1 to 5
move 1 from 4 to 3
move 1 from 3 to 9
move 4 from 2 to 4
move 4 from 8 to 7
move 3 from 2 to 6
move 1 from 2 to 7
move 5 from 5 to 6
move 1 from 5 to 8
move 5 from 8 to 7
move 7 from 4 to 6
move 15 from 6 to 4
move 1 from 8 to 7
move 1 from 1 to 5
move 1 from 2 to 4
move 2 from 4 to 8
move 1 from 5 to 2
move 5 from 6 to 4
move 2 from 2 to 1
move 1 from 9 to 4
move 1 from 6 to 9
move 3 from 9 to 3
move 3 from 4 to 3
move 1 from 6 to 1
move 5 from 3 to 4
move 2 from 8 to 5
move 1 from 3 to 6
move 1 from 6 to 2
move 1 from 2 to 8
move 6 from 4 to 2
move 1 from 2 to 7
move 1 from 5 to 3
move 4 from 9 to 3
move 1 from 9 to 1
move 3 from 1 to 6
move 1 from 9 to 7
move 14 from 7 to 6
move 1 from 8 to 3
move 4 from 2 to 6
move 3 from 3 to 8
move 9 from 4 to 9
move 1 from 1 to 5
move 2 from 5 to 8
move 3 from 8 to 2
move 4 from 2 to 6
move 1 from 3 to 9
move 10 from 6 to 1
move 5 from 9 to 8
move 1 from 9 to 3
move 6 from 1 to 8
move 3 from 7 to 4
move 2 from 4 to 5
move 2 from 9 to 8
move 15 from 8 to 3
move 3 from 7 to 9
move 8 from 4 to 3
move 2 from 5 to 9
move 6 from 6 to 5
move 6 from 5 to 8
move 1 from 7 to 8
move 6 from 9 to 2
move 5 from 2 to 4
move 6 from 3 to 5
move 5 from 5 to 8
move 1 from 5 to 7
move 1 from 9 to 7
move 2 from 6 to 4
move 12 from 8 to 2
move 7 from 2 to 4
move 3 from 7 to 5
move 3 from 5 to 7
move 3 from 7 to 9
move 2 from 9 to 7
move 1 from 9 to 3
move 2 from 7 to 4
move 3 from 1 to 9
move 4 from 6 to 5
move 6 from 2 to 8
move 14 from 4 to 9
move 7 from 9 to 6
move 9 from 9 to 2
move 1 from 5 to 8
move 5 from 6 to 3
move 3 from 1 to 9
move 3 from 8 to 9
move 1 from 8 to 3
move 5 from 2 to 5
move 1 from 4 to 9
move 2 from 6 to 1
move 2 from 3 to 6
move 3 from 8 to 3
move 2 from 6 to 3
move 1 from 4 to 9
move 4 from 3 to 6
move 7 from 6 to 9
move 10 from 9 to 2
move 10 from 3 to 2
move 7 from 2 to 8
move 2 from 1 to 7
move 13 from 3 to 7
move 7 from 5 to 1
move 1 from 9 to 6
move 4 from 8 to 4
move 2 from 3 to 2
move 4 from 4 to 6
move 1 from 3 to 4
move 5 from 6 to 5
move 3 from 5 to 7
move 12 from 2 to 5
move 7 from 5 to 6
move 2 from 8 to 3
move 7 from 6 to 2
move 3 from 9 to 6
move 1 from 6 to 7
move 1 from 4 to 9
move 2 from 7 to 6
move 13 from 7 to 4
move 3 from 7 to 5
move 1 from 9 to 6
move 12 from 4 to 3
move 1 from 8 to 1
move 2 from 6 to 4
move 1 from 7 to 9
move 2 from 9 to 8
move 12 from 3 to 5
move 1 from 8 to 2
move 15 from 5 to 6
move 2 from 4 to 6
move 1 from 9 to 6
move 5 from 5 to 4
move 4 from 4 to 2
move 2 from 1 to 5
move 4 from 1 to 5
move 1 from 8 to 6
move 7 from 5 to 2
move 22 from 2 to 3
move 9 from 6 to 3
move 1 from 1 to 8
move 1 from 8 to 7
move 23 from 3 to 6
move 2 from 2 to 4
move 1 from 7 to 8
move 1 from 8 to 2
move 19 from 6 to 9
move 2 from 2 to 4
move 4 from 4 to 6
move 13 from 6 to 8
move 12 from 9 to 1
move 2 from 5 to 9
move 2 from 4 to 8
move 1 from 2 to 7
move 1 from 7 to 1
move 4 from 6 to 2
move 10 from 1 to 9
move 1 from 6 to 7
move 11 from 8 to 2
move 6 from 3 to 6
move 1 from 7 to 2
move 1 from 1 to 8
move 2 from 6 to 7
move 7 from 6 to 3
move 9 from 3 to 1
move 7 from 9 to 6
move 1 from 8 to 7
move 4 from 2 to 6
move 1 from 8 to 3
move 6 from 6 to 5
move 9 from 9 to 3
move 5 from 6 to 1
move 1 from 7 to 8
move 2 from 8 to 4
move 1 from 4 to 2
move 1 from 4 to 5
move 2 from 5 to 6
move 1 from 6 to 9
move 9 from 1 to 4
move 4 from 4 to 6
move 2 from 4 to 7
move 7 from 2 to 8
move 5 from 6 to 7
move 6 from 3 to 8
move 8 from 1 to 9
move 3 from 5 to 2
move 2 from 3 to 9
move 3 from 9 to 4
move 7 from 2 to 3
move 1 from 7 to 2
move 10 from 3 to 2
move 6 from 9 to 4
move 1 from 3 to 1
move 1 from 1 to 8
move 4 from 8 to 5
move 10 from 8 to 4
move 2 from 8 to 9
move 7 from 4 to 9
move 6 from 2 to 6
move 3 from 6 to 5
move 4 from 4 to 9
move 8 from 7 to 5
move 1 from 9 to 2
move 7 from 2 to 1
move 4 from 9 to 8
move 2 from 6 to 3
move 2 from 3 to 2
move 13 from 5 to 7
move 5 from 4 to 9
move 5 from 1 to 7
move 3 from 5 to 8
move 17 from 7 to 2
move 15 from 2 to 6
move 15 from 9 to 5
move 1 from 9 to 5
move 4 from 8 to 6
move 1 from 4 to 6
move 5 from 4 to 7
move 5 from 2 to 7
move 18 from 6 to 2
move 2 from 7 to 6
move 10 from 2 to 8
move 2 from 2 to 3
move 11 from 8 to 7
move 7 from 7 to 5
move 9 from 7 to 5
move 3 from 7 to 5
move 2 from 1 to 7
move 4 from 2 to 1
move 30 from 5 to 1
move 1 from 3 to 1
move 35 from 1 to 9
move 2 from 2 to 5
move 2 from 8 to 3
move 20 from 9 to 2
move 3 from 7 to 9
move 1 from 3 to 6
move 5 from 5 to 3
move 18 from 2 to 5
move 4 from 5 to 8
move 7 from 9 to 7
move 1 from 6 to 2
move 3 from 8 to 5
move 6 from 3 to 5
move 3 from 7 to 4
move 2 from 2 to 3
move 1 from 4 to 5
move 2 from 4 to 5
move 4 from 7 to 2
move 26 from 5 to 6
move 2 from 2 to 7
move 1 from 2 to 9
move 1 from 7 to 8
move 1 from 5 to 3
move 2 from 8 to 3
move 11 from 9 to 3
move 6 from 3 to 4
move 27 from 6 to 4
move 33 from 4 to 3
move 4 from 6 to 8
move 1 from 2 to 8
move 1 from 7 to 3
move 4 from 8 to 9
move 1 from 8 to 6
move 34 from 3 to 8
move 1 from 8 to 5
move 1 from 2 to 9
move 8 from 3 to 9
move 3 from 5 to 4
move 1 from 6 to 5
move 27 from 8 to 9
move 1 from 3 to 4
move 1 from 5 to 7
move 3 from 8 to 1
move 11 from 9 to 1
move 1 from 7 to 5
move 11 from 9 to 3
move 1 from 5 to 1
move 1 from 8 to 7
move 2 from 9 to 2
move 1 from 2 to 1
move 1 from 2 to 7
move 2 from 8 to 2
move 6 from 3 to 8
move 1 from 4 to 2
move 7 from 1 to 2
move 1 from 7 to 1
move 19 from 9 to 1
move 3 from 2 to 9
move 10 from 1 to 4
move 2 from 9 to 1
move 1 from 7 to 9
move 7 from 1 to 6
move 10 from 4 to 3
move 14 from 1 to 7
move 2 from 9 to 1
move 3 from 4 to 6
move 9 from 7 to 6
move 1 from 3 to 5
move 4 from 8 to 5
move 10 from 6 to 8
move 3 from 5 to 6
move 10 from 3 to 4
move 4 from 3 to 7
move 1 from 5 to 9
move 2 from 7 to 9
move 1 from 1 to 9
move 6 from 2 to 4
move 1 from 5 to 3
move 11 from 4 to 9
move 3 from 4 to 9
move 1 from 2 to 7
move 2 from 3 to 5
move 1 from 3 to 2
move 7 from 7 to 2
move 2 from 5 to 8
move 8 from 2 to 1
move 2 from 6 to 8
move 9 from 6 to 8
move 3 from 8 to 2
move 3 from 2 to 6
move 9 from 9 to 5
move 3 from 5 to 8
move 5 from 9 to 4
move 3 from 6 to 4
move 1 from 6 to 3
move 3 from 1 to 6
move 3 from 6 to 9
move 17 from 8 to 5
move 12 from 5 to 4
move 21 from 4 to 3
move 1 from 4 to 9
move 7 from 5 to 4
move 22 from 3 to 7
move 3 from 1 to 8
move 3 from 9 to 1
move 4 from 4 to 6
move 1 from 6 to 2
move 3 from 4 to 1
move 1 from 6 to 7
move 4 from 9 to 3
move 2 from 5 to 7
move 1 from 9 to 6
move 2 from 6 to 9
move 8 from 7 to 9
move 1 from 6 to 2
move 1 from 9 to 3
move 4 from 3 to 4
move 14 from 7 to 4
move 1 from 3 to 2
move 3 from 7 to 8
move 12 from 8 to 9
move 8 from 4 to 1
move 1 from 7 to 4
move 2 from 5 to 1
move 3 from 2 to 9
move 17 from 9 to 3
move 6 from 9 to 1
move 1 from 9 to 2
move 13 from 3 to 9
move 4 from 3 to 1
move 3 from 9 to 1
move 22 from 1 to 9
move 1 from 8 to 1
move 6 from 9 to 5
move 4 from 1 to 9
move 3 from 1 to 9
move 4 from 4 to 8
move 4 from 4 to 2
move 1 from 4 to 3
move 3 from 8 to 9
move 1 from 3 to 4
move 1 from 1 to 3
move 1 from 8 to 2
move 1 from 5 to 8
move 4 from 2 to 1
move 1 from 8 to 7
move 10 from 9 to 6
move 1 from 7 to 9
move 1 from 2 to 3
move 1 from 6 to 1
move 3 from 5 to 7
move 1 from 8 to 7
move 1 from 6 to 1
move 1 from 2 to 4
move 1 from 5 to 2
move 19 from 9 to 2
move 1 from 4 to 7
move 1 from 3 to 7
move 3 from 7 to 9
move 4 from 1 to 2
move 10 from 9 to 4
move 1 from 5 to 8
move 3 from 6 to 4
move 1 from 3 to 4
move 10 from 2 to 8
move 12 from 2 to 5
move 3 from 5 to 9
move 5 from 6 to 5
move 5 from 1 to 4
move 22 from 4 to 3
move 3 from 8 to 7
move 1 from 7 to 2
move 3 from 2 to 9
move 19 from 3 to 5
move 2 from 7 to 8
move 7 from 5 to 6
move 5 from 9 to 6
move 1 from 9 to 3
move 16 from 5 to 1
move 2 from 3 to 1
move 3 from 7 to 3
move 7 from 8 to 4
move 2 from 8 to 1
move 5 from 5 to 9
move 1 from 5 to 2
move 1 from 2 to 3
move 1 from 8 to 5
move 4 from 5 to 7
move 2 from 3 to 8
move 2 from 1 to 5
move 4 from 7 to 6
move 6 from 4 to 7
move 4 from 9 to 8
move 14 from 6 to 7
move 8 from 1 to 7
move 7 from 1 to 3
move 3 from 5 to 9
move 28 from 7 to 5
move 1 from 1 to 8
move 4 from 8 to 3
move 9 from 3 to 1
move 1 from 9 to 5
move 6 from 3 to 2
move 10 from 1 to 6
move 1 from 1 to 9
move 5 from 9 to 7
move 14 from 5 to 3
move 1 from 4 to 1
move 1 from 7 to 2
move 1 from 7 to 1
move 1 from 1 to 7
move 3 from 8 to 5
move 4 from 6 to 3
move 3 from 7 to 2
move 15 from 3 to 6
move 16 from 5 to 7
move 4 from 2 to 8
move 1 from 3 to 1
move 5 from 7 to 3
move 12 from 6 to 4
move 4 from 8 to 5
move 1 from 4 to 2
move 2 from 5 to 3
move 8 from 6 to 3
move 7 from 4 to 5
move 9 from 7 to 6
move 1 from 7 to 9
move 1 from 1 to 9
move 1 from 1 to 9
move 5 from 2 to 8
move 5 from 8 to 2
move 11 from 5 to 9
move 1 from 4 to 2
move 4 from 9 to 6
move 12 from 3 to 7
move 3 from 4 to 9
move 14 from 6 to 2
move 2 from 2 to 4
move 2 from 3 to 5
move 10 from 7 to 2
move 1 from 4 to 8
move 1 from 2 to 7
move 28 from 2 to 9
move 4 from 7 to 5
move 1 from 2 to 4
move 6 from 5 to 1
move 2 from 4 to 3
move 1 from 8 to 1
move 40 from 9 to 1
move 10 from 1 to 6
move 5 from 3 to 5
move 1 from 9 to 8
move 3 from 6 to 7
move 11 from 1 to 2
move 9 from 2 to 3
move 3 from 5 to 1
move 4 from 7 to 1
move 2 from 2 to 4
move 2 from 5 to 8
move 19 from 1 to 7
move 8 from 3 to 2
move 14 from 1 to 8
move 14 from 7 to 1
move 4 from 6 to 5
move 1 from 1 to 9
""")
