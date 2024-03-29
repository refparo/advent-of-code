from collections import deque
from itertools import count

surrounding = [
  (dx, dy)
  for dx in [-1, 0, 1]
  for dy in [-1, 0, 1]
  if dx != 0 or dy != 0
]

def solve(input: str):
  elves: set[tuple[int, int]] = set()
  for y, line in enumerate(input.strip().splitlines()):
    for x, c in enumerate(line):
      if c == '#': elves.add((x, y))
  directions: deque[tuple[int, int]] = deque([(0, -1), (0, 1), (-1, 0), (1, 0)])
  proposal: dict[tuple[int, int], list[tuple[int, int]]] = {}
  def area():
    xmin, ymin = min(x for (x, _) in elves), min(y for (_, y) in elves)
    xmax, ymax = max(x for (x, _) in elves), max(y for (_, y) in elves)
    return (xmax - xmin + 1) * (ymax - ymin + 1) - len(elves)
  for round in count(1):
    for (x, y) in elves:
      if elves.isdisjoint((x + dx, y + dy) for (dx, dy) in surrounding):
        proposal[(x, y)] = [(x, y)]
        continue
      can_propose = False
      for (dx, dy) in directions:
        match (dx, dy):
          case (dx, 0):
            if elves.isdisjoint((x + dx, y + dy) for dy in [-1, 0, 1]):
              proposal.setdefault((x + dx, y), []).append((x, y))
              can_propose = True
              break
          case (0, dy):
            if elves.isdisjoint((x + dx, y + dy) for dx in [-1, 0, 1]):
              proposal.setdefault((x, y + dy), []).append((x, y))
              can_propose = True
              break
          case _: raise Exception()
      if not can_propose:
        proposal[(x, y)] = [(x, y)]
    elves.clear()
    nobody_move = True
    for (x1, y1), proponents in proposal.items():
      if len(proponents) == 1:
        if nobody_move and (x1, y1) != proponents[0]:
          nobody_move = False
        elves.add((x1, y1))
      else:
        for elf in proponents:
          elves.add(elf)
    if round == 10:
      print(area(), end=" ")
    if nobody_move:
      print(round)
      break
    proposal.clear()
    directions.rotate(-1)

solve("""
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""")

solve("""
...####..#.#.#....###..#....#..#..#...##..###..##.#...######.##....####
..#.##..#.#...###..###.##....#..##......#.###..###....#.#.#....#...#.#.
.##...#...####..####....#....#####.##.#.....#.#.#.#..#..#...####....###
.####..#.##...#.##..#.#...#..#..##.######.#######.###.##.....####.#.##.
##.##.#..######.####..##...##.#.##...###.###..#.#..####..##...###.##.#.
...###.#.###..####..###.##..#..###..#..##.###.##.##....##...##.#.#..##.
###.##...#...#.#..####..##.#..###.##..#..##.#...#...##..##..##.##.###.#
..##....###.##.#...#####.#.#.###.#.#.#.##.#...#####.#####.....###.....#
#.####.#...#.#...##..#..#.#...###.#.####.#..##..##.#.###...#.####....##
#.##...#.#####...##....##..###..#...##.###..#.#.##.##.....#####....#...
#...#..#..#.#...##..#####.#.###......##..##.##.##...###..###...#..###..
..#.##.#..##.##.####.....#.###..#..#..#...###.###..#.#.##.##..#####..##
.##.#...#.....####......#.#..#..#.#....#.#...####...##.#.#.....#.#.....
#..#.##..###..#.....#.###..#.#..........##.......##.##.#..######...###.
.#...##.#.#...##.####..######.###.#.#.#.####.##.###..#...###.#..#..##.#
#.#.##.#.###..##.###.##.....###.#.#...#...###.##.#.#.##.##.#####.....#.
.#...###.##...#.##.#.###.###.##......##...##.#.###..#..#.#.##...####.#.
.#.#.##..#...#.##..#..##.....#....#....#.###....#########..#.#.########
.#.##..###..##..#.......##.##..#..###.#.##.####....#..#.#...##..##.#...
#####.##.#.....#.##...#.#...#.#.####..####....#.#...#.....###...##.....
..###....#....##...#.#...###....##.###.#.#...##..##.#..#.##....#.#.#.##
########..####...#.#..##.###...##.#...#...#.######...#..#..#..#...#..##
#.#....##...##..#...#....#.##....#.###.##.#...###.#..#.#.#...###..#.#.#
#.##........#..##...#...##.##.###.#.##...##...#####.#.#.....####.#.#..#
##.##...####.##.#...#....#...###.#...#....#.#.#.####...#.#....#.####.#.
.###....#..#.#..#..####..###.#.#..#.#..#.####..#####..#.#.#..#.....##.#
.#####.#.##.###......#..##.#.....#######..##.##.#####....#..#.#..####.#
.#....###....#.##..##.#.#.#.....#####..#.#.#.##...#.#....#.##..##....#.
####....####...#.#...#..##....#.#.#.###..#.######.##..##..######...#.#.
.#..####..#####.###..#..##.#.####.##.##..#.###..#...##.#...#.#.#.#.#.##
#.###########.####.....###.#..#...###.#######...#.#...##..###....#....#
#..#.####...###..####.#.##.#.#.#.#####.###.####...#...#....########..#.
#######.#..#.#..####.##.##..##.#...##..#######..#.#..#...#..##..#.###.#
##.#.....###.#..####.##..#.#######.#.#..#.##.#..###.##..##.##.#...#.#.#
#.#######.#.##.#.###.##.##...##..#.#....#.#.#..#.#..###..##.#.#.....##.
.##.##.#...####.#####.####.####.....#..####..#..##..###...#.#.###.#...#
.####...#..#.#.#.#........#..###...#####..####..##..######.###...#####.
###....#..##.##..#####....##.#..#...##.#####..#..###.#####..###.#..##.#
..#.#...#.##..#.##.####.####..#######....##....#.#....#.#.#..##.#.#..##
.#..#.########.........###.#.....###.######..#.######...####..#..#.#.##
.#.#...###...#.#.#.#..#...##.###.#.#.##.##.....####......##.#.#....##.#
..##..##...#.#######.#.##.####.###.#..#.....#.#..#...#..####..##..#.###
.#...####.##....###..#.###...###.##...###..######.#.#.#.#.#.#.#....#.##
.###..#.###.###..##.#..##..#.#.#...#..#.#..#...##..#..#...###...#####.#
#.#..#.#.#.....##..#.##..##.#.....#..###..#.#.#.#.#.#.##..#.####..##...
..#.#.####...#.##..##.##.####..##.#.#..##.#.###.#.######..#.######.#...
###.#.#.#.####..##.######.#.#...##......###..###.#..#...#...#.#..######
.###.#..#..######..##.####.###..##.#...#.#.#......###..##.#.#....#.#.#.
.##..#...#....#..###.##.#..#####.#.#....######..#....#..######.....#...
#.#...#..#.##...#..#..###.......####...#.####...#.#.#....#####.##...#.#
....#.####.#...#..#####.#..###..######.###.....#..#.#.#.#.#.##.#.##....
#.......#####.#.###..##.###..#####..#.###..#.....#.###.###..###..#.##.#
##.#.#....##.#.#..#..#...###.#..#.....###...###...#..#.######.#.#...##.
#....####.##.###....#....#....#...#..####...#.#.#.###..##.#.#..##.#..##
#.....#.##....###..####..##.#.......#..#.#.#.....#....####.#...#....###
###.#..####....#.....#..####....######.....#.#....#..###.#.#..#.#..###.
#..#.#.#...##....##.##....##.....#..####.###..##.#.#.##..#.##.###...###
....###.#.#.#..###.#.##.#.#.#.#####.#####..#..##...##.##.#...####.#.###
#####.....#.#.#.#.#.#.###.#####.#...#.##..#.#.##..##..###...#...#..##..
##.####.#.#.##..##.##.###....##.#..###.####..#######.#...##....#..##.##
##..#.####.##..#..#.#.#####.#.#.....#####..##..#.##.....##..#.#....##.#
.#..####...####.#####.##..#.##.....###.###.#.#.######..####.#...#..#.#.
##.####..##..#.....##.#.####..#..#....##...#....#####..##########.###.#
#...#.#.....#####.......###.#.#.#.###....#.#..#..#.##..#..#..#.####.###
##.###..#..##......##########....###..#######..#....#.#..###.##........
####.........#.#...##.#.#.#..#.#.####.#####....##...#.#.##.###..#.##.##
.####.#...#..#.##.####..##..#..#...##...........##..###.####..##..#.#..
.#####.##....##.#..####.##..##.#.###.....##.#..#..#.#.#...#.#...####...
#...####........#.##.####..##.....#####.#.#####.#####..#.##.#..##...##.
.###..###.####..###..##..##.#..##.###.#...#..#...#..#...#..#######.#.##
.#..#..##...##....##....####..#....#.##.....#.##..#.#..#...#..##.#..#.#
""")
