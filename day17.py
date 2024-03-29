from itertools import cycle

def gen_moved_rocks(rock: list[int]):
  yield rock
  while all(line & 0b000000001 == 0 for line in rock):
    rock = [line >> 1 for line in rock]
    yield rock

# rock_types[type][x][y]
# x = 0 and x = 8 are the walls
rock_types = [
  list(gen_moved_rocks(list(reversed(rock))))
  for rock in [
    [
      0b111100000
    ],
    [
      0b010000000,
      0b111000000,
      0b010000000
    ],
    [
      0b001000000,
      0b001000000,
      0b111000000
    ],
    [
      0b100000000,
      0b100000000,
      0b100000000,
      0b100000000
    ],
    [
      0b110000000,
      0b110000000
    ]
  ]
]

def collided(chamber: list[int], rock: list[int], y: int):
  return any(c & r != 0 for c, r in zip(chamber[y:], rock))

def solve(input: str):
  jets = enumerate(cycle(input))
  rocks = enumerate(cycle(rock_types))
  chamber = [0b111111111]
  height = 1 # height of the tower, including the floor
  mem: dict[str, list[tuple[int, int, int]]] = {}
  height_skipped = 0
  target_skipped = 0
  part1_chkpoint = False
  part2_chkpoint = False
  while True:
    rock_idx, rock = next(rocks)
    x = 3
    y = height + 3 # rock[0] overlaps with chamber[y]
    while len(chamber) < y + len(rock[x]):
      chamber.append(0b100000001)
    while True:
      # jet blows
      jet_idx, jet = next(jets)
      new_x = x - 1 if jet == "<" else x + 1
      if not collided(chamber, rock[new_x], y): x = new_x
      # rock falls
      y -= 1
      # test if falls to ground
      if collided(chamber, rock[x], y):
        y += 1
        break
    # add rock to chamber
    for z in range(y, y + len(rock[x])):
      chamber[z] |= rock[x][z - y]
    # increase height
    height = max(height, y + len(rock[x]))
    # print part1 answer
    if rock_idx + 1 == 2022:
      print("part 1:", height - 1)
      part1_chkpoint = True
    if target_skipped == 0:
      # find repeating pattern
      cutoff = 0
      for i in reversed(range(y - 1, y + len(rock[x]))):
        if chamber[i] | chamber[i + 1] == 0b111111111:
          cutoff = i
          break
      if cutoff != 0:
        pattern = "\n".join(f"{line:09b}" for line in chamber[cutoff:height])
        mem.setdefault(pattern, [])
        for r, j, h in mem[pattern]:
          if (rock_idx - r) % 5 == 0 and (jet_idx - j) % len(input) == 0:
            # found!
            actual_remaining = 1000000000000 - (rock_idx + 1)
            target_skipped = rock_idx + actual_remaining % (rock_idx - r)
            repeat = actual_remaining // (rock_idx - r)
            height_skipped = repeat * (height - h)
        if target_skipped == 0:
          mem[pattern].append((rock_idx, jet_idx, height))
    elif rock_idx == target_skipped:
      print("part 2:", height_skipped + height - 1)
      part2_chkpoint = True
    if part1_chkpoint and part2_chkpoint: break

solve(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
solve(">>><<>>><><<>>>><<<>><>>><<<<>>>><<><<>>><<<<><>>>><<<<>>><<>><>><<<>>>><><<<>>>><<>><<>>><<<>>><<>>>><>>>><<<>>>><<<<><>>>><<<<>><<<<>>><>><>>>><>>>><><<<>>>><<<<>>>><<>>>><<<<>>><<<>>><<<<><<>><<<><<<>>>><>><>>>><<<<>><>>><<>>><<><<>>>><<<<>>><<>>><>>><>>>><<<<>><<<>><<<<>>>><<>>><<><<>><<>><>><<>>>><><<<<>>>><<><>><><<>><<<<>><<<<>>><<<<>>>><>>><><<<>>>><<<<>><<>><<<<>>>><<<<>>><>>>><<<><<><<>><><<>>><>>>><<>>><<<<><<<><>>><>><<<>>><<<>>>><<<>>><<>>>><<<>><<<<>>>><<<>>><<<><<<<><<<>>><>><>>>><<<<><<>>><<<<>>><<><<<<><<<>><<>><>><<<<>>><<<>>><<<<><<>>><<<<><<<><<<<>>><<<<>>>><<>>><<><<<<>>>><<>>><<><<<><<>><<<<><<<>>><<<<>>>><<>><<<<>><>><>><>>><><<<>><<>><>>><>><<<><>>>><>>><<><>>><<>>>><>>>><>><<>>>><>><<<<><<<<>>><<<<>><<>>><>>><<<<><<<<>>>><<<<>><<<<>>>><<<<>><<<><<<>>><<><<>>>><>><<<<>>><<>>>><<<>><<<>>>><<>><<><<<<>>>><><<<<>>>><><<>><<<<>>><<>>>><<<<>>>><><>><<<>>><<<<><<<>><<>>>><<<>>><<<<>>>><>>><>>><<>>>><<<>>>><<<>>><<>>>><<>><<>>><>><<<>>><<<>>>><<<>><<<<><<<>>><<<>>><<>><<<>><<<<>>><<>>>><<<<>>>><>>><>><<<>><<<><<<<><>><<<<>>><<<<><>>>><<<>><<<><<<<><<<<>>>><<<<>><<<>><<<><<>><<<>>><<<<><<>>>><<>>><<>>>><>>>><<<>>><<<>><<<<>><<<><>><><<<<>>><>>>><<>><<<<>><>>>><<<>><<><>>>><<<<>><>>>><<>>><<<<>><>>><>>>><>>><<<><<<>>><<><<>>>><<<<><><<<<>><<<>>><<<><<>><<>><<<<><<>>><<>><<<<><<>><<<>><>>><>><<<<>><<<>><<<>>>><<<>>>><<<<>>>><>><><<<>>>><<<><<<>>><<>>><<>><<<>>><>>>><<<><>>><<><>>>><>><>><<<<>>>><<>><>>>><<>>><>>><<>>><>>>><<<>><<>>>><<<>>>><<><<<<>>><>>><>>><<<>>><<>>><<<<>>><<<>><>>><<<>>>><>>>><>><<<<>>><>>><>>><>>><<<<>>><<><<<>><<<>>><<<<>>><<<><<<>>><>><><>><<>>><<<<>>>><<<>>><<<><<<>>>><<<>>><<<<>>><<<<>>><<<<>>>><>>><<><<>><<>>><<<<>>><<>><<<<>>>><<<><>>>><<<>>>><<<>><<>><<><<>>>><<<<>><<>><<<<><<<<><<<<>>>><<>>>><<<>>><><<<<>>><>>><<>>>><<<>>>><<<>><>>>><<<<>>>><<<><<<>>>><<><<<<>>>><<>>>><<>><<><<<<><<>><<><<<<>>>><>><<<>>>><><<>>>><>>>><>>><<<<>><<><<<>><<>>>><><<><<>>><>><<<><<<>><<<<>><<>>><<<><<<<>>>><>>>><>><>>>><<<>><<><<<<><>>>><<>><<<>>><<<>>><<<>><<<<><><<<>>><<<<>><<<>>>><><<>>>><<>><<<>>><<<<><<<<><>><<>><><<><<>>>><<<>><><<><>><<<<><>><>><>>><<<>><<<>>>><<>><<>><<<<>><>>>><<<<>><>>>><<<<>>><><<<>>><<>><<<>>><<<<><<<>>><<>>>><<<>>><>>>><<<<>>><><>><><><<<>>>><>>>><<<>>><><<><<>>>><<<<>>><>><<<<>>>><>>>><>><>>><<<<>>><<>>><>>><<><<<><>><<><<>>>><<<<>><<>><<<<>>><<<><<><<>>><<<<>>>><<<<>>><<>>>><<<>>><<<<>>>><<<<>>>><<<<>><<<>>><<<<>>><<<>>><<<>><<<>>>><<<<>>>><>>><>>>><<<>>><<<>><<<><<><>>>><<><<>><<<<>>><><<<<><<>>>><<><<<>>><<>><<<<><>>><<>>><<<>>>><<><<<>>>><<><<>>>><><>>>><<>>><>><<>><<>><<><<<<>>>><<<><>><<<<><<<<>><<>><<<>>><<><<><<<<>>>><<<><<<<>>>><<<>><<>>>><<<>><<>><>><><<<>>>><<><<<<>>>><<<>>><<<>>><>>><<<>>><<<>>><<<><<>>><<>>><<<<><<<>><<<>>><<<<>>><<<<>><<<>>>><>><<<>>>><<>><<><<>>>><<<><<>>><<><<<><<<<><>>>><<>>>><<<<>><>><<<<>>><<<<>><>><<<<><><<>>><><<>><<<<>><>>><>>><<<<>>>><<<<><<>><><<<>><><<<<>>><>>>><<<>>>><>><>>>><<<>>>><<>>><<<<>>><<><>>><<<<><<<>>>><<>><<<<><<<>><<>>>><<><><<>><<<>>>><<<>><<><<<>>><<>>><>>><>>>><<>>><<<<>><<<><<>>><<<><<>>><>>><<<<>><<<>>><<>><<<<>><<><<>>><<>><<<><>>>><>><<<><>>><<>>>><<>><><<<<><<<><<<><<<>>><<<>>><<<<>><<<><><>><<<>>>><<>>><<<>><<>>><><>>><>><>>>><<>><<>>><<><<<>>><<<>>>><<<>><<<>>>><>><<><><<><<<<>><<<<>><<>>><<<><>>><<<><<<<>>><<<><<<>>>><<>><<<<>><<<><<>>>><<>><<<<>><<>><<>>><<<<>><<>><><<<><<<>><<<<><<>><>>>><<<>>><>>><<<>>>><<>>>><>>>><<<<>>>><>>>><>>><<<>>>><<>><<<><><<<><<<>>>><<<>>>><<<<>><<<>>>><<<>>>><<<>><><<<<>>>><>>><<<<>>>><<<<><>>><<<<><<<><<<<>>>><><<>>><<<<><<>>><>>><<>>>><>><<<<>>><<<>><>>><<><<<>>><<<<>>><<>>><<<>>><<>>>><<<<>>>><>>>><<<>><<<<>>><<><>><<>>><<<<><<>><<<<><<>>><<<<><<<><<<>>><<><>><<<<>>><<<<>><<<<>>><<><><>>>><>>><<<>>><><>>>><<<>>><>>>><<<>>>><<<>><<>>><<<>>><>>>><>>>><>>><<>>><<<><>><<<>>><<<>>><<<<>>>><<>>><<<<>><<<<>>><<<<><<<<>>><<>><<<<><<>>><<<>>>><<<>><<<><<>>>><<<>>>><><<>>><>>>><<<>><<<>>>><<<<>><>>>><<><<<>>>><<<<>><<<<>>><<>>><<<>>><><<<>>>><<<><<<><>><>>><><<<>>><><<<<>>>><<<<>>>><<<>>>><>>><<>>><>><<<<>>>><<>><<<<><<<<>><>>><<<<><<<<>><<<>>>><<<><<<<><<<<><>>><<<>>><<<<>><<<>>><<><<>>><<<>>><>><<><<>>><<<<>>>><><>>><<<><<<>><<<<>>><<<>><<>><<<>>><<<<><<<<>>>><<<<>><<>><<>>>><<><<<>>>><<<>>>><<<<>>><<<<><>>>><>>><<><<>>><<<>>>><>><<<><<>>>><<><<<>>><>><<>>><<<<>>>><<<>>>><>>><<><<<<><<><>>><<>><<>><<>><<<<>><<<<>>>><<<<>><<<><<>>>><>>>><>>><<<<>><<<><<>>><>>><>><<<>><><<>><<>>>><<><<<<><<<<>>><<>>>><<>><<<><<<<><<>>><<><<<>>>><<<<><>>>><<<<>>>><>>>><<>>>><>><>>><<><<<><<>>>><<<><<><<>>><<><<<<><<<>><<<<>><<><<<>><<<><<<>>><<>><<<>>><<<>>>><>>>><<<>>>><<>><><<>>>><<<<>><<<<>><<<>>>><><<>>>><<<>>>><<<>>>><<>><<<<>>><<<<>><<<>>>><>>><<<<>>><<<>>><><<<<>>><<<>><<>>>><<<>>><<<<>>><<>>>><<>>><<<<>>>><>>><<><<<<>>>><<<>>>><<<<>>><><<<<>><<<<>>><<>>><<<<>>>><<<><<<<>><<<<>>>><<>>><>><><<<>>><<<><>>><>>>><<<><><<><><>><<><>>><<<<>><<>>><<<>>>><>>>><<<<><<<>>><<<<>><<<><>>>><<<<>>><<<<>><<<<><<<<>><<<>>><<<>>><<>>>><>>><<>>>><<<><<><<>>>><<>><<><<<<>>>><><<>><<<>>><>><<<<><<<<>>><<>>><<>><<<>>><<<>><<>>><<<<>>><>>><>>>><>>><>>><>>>><<>><<<<>><<<<>>>><<<<><<<>>><<>>>><<<><<><<<>>><<>>>><<><><>>>><<<>>>><>><<><<<<><>>><>>>><<<>><<<<><<<<><>>><<<<><<>><<<<>>>><<<>>><<<><>>><<><<<<>><>>><<<<>>><<<>>><>>>><<<<>>>><>><<>>><<<><<><<<<>><<<>>>><><<<>><<<>>><<<><<>>><<<>><<<<>>>><<><<>><>><<>>>><<<>>><<>>><<<>>><>>>><>>>><<>>><<<>>>><>><>>>><<<>>>><><<><<<<>><><<>>><<<>>>><<<<><<<<>><<<<>>>><<<<>>><>>><>>><<>>>><><<><<<>>><<>>>><<<>>>><>>>><<>>>><<<><<><<<<>>>><<>>><<<<><<<><<>>>><<<<><<>>><>>>><<>>><<<<><<>><<<<>><<<>><<<><<<<><<<>>><>><<<>>>><<<<>>>><<<<>><<<<>><>><>>>><>>>><<>>><<<><>>><><<<<>>>><<>>><<><<<>>>><<>><<>><<<<>><<<<>>><<<><<>>><<<<>>>><<<>>>><<<>><<<<>><<<>>>><<<<>><>>>><<><<<>><<<><<<>>>><<<>>><<>>><<>>>><<<>>>><>>><<<<>>><>>>><<<>>>><<<><<>>><<<<>><<<>><>><>>><>>>><<><<<>>>><<<><<<><<<<><<<>>><<<<>>><>><<>>>><<<>><<<>>><<>>><>><<<<>>><<><<<<>><<>>>><<<<><<><>>>><<<>>><<<>><>><><<<<>>>><<<<><<<>>><<>><<>>><<<>>><>>><<<<>>>><<<>>><>><<><<<>>>><<<>>>><<<<>>>><<<><<<>>>><<<><<<>>><><<<>>><<>>><><<>>><>>>><<<>>><><<<<>>><<><<<>><>>><>><<<<>>><<<<><<<>>><>><<<<>>><<<>><<><<<<><<<><<>>>><<<<>><<>><<<><<>>>><<>>><<>>>><<<<>><<<<>>><<>>>><>>>><<<<>>><<<>>>><<<>>><>><<<<>>>><<<<>>>><<<><>>><<<<><<<<><<><<<>><<<<>>>><<>>>><<<>><<<<>>>><>>>><<<<>><<<>><<<<>>>><<<>>>><<<>>><>>><>>><<>>><<<>>><>>><<<<>>><<><<>><<<>>><<<<>>>><<<>><<<>><>><<<><<>>><<<<>>><<>><<>>><<<>>>><<<<><><>>>><>><<<>><<<<><<<<>>><<<>><<>><<>><<><<<>>>><>><<><<<<>><<<<>>>><<<<><<<<>><<<<><<<<><<<>>>><<<><<<>>><<<>>><>>><<>>>><<<<>>><>>>><<<<>><<<<><<<><<<><>><><<<<>>>><<>>>><<<<>>>><<>>><<<<>>>><<<>>>><<>>><<<<><<>><<<<><>>>><<<>>>><><<<<>>><<>>><<><<<>>><<>><>>><<>><><<<<>><<<<><<>><>>>><>>>><<>><<<>>><<<<>><<<>>><<<><<<<>>><>>><<>><<<<>>>><<<<>>>><>>>><<<<><>>>><<<<><<<>><<<<>>><>>><>><><<<>>>><<>>><<<<>><>><<<>><<>>><>><<>>><<>>><>>><>><<>>>><>>>><<<>>>><<<>>><>><<><<>>>><<>><<<<>>><<><><<>>>><<<>><>>>><<<>><<<<>>><<<<>><<>>>><<<>>><<<<><>>>><><<<>>><<<<>>><<<<>>><>>><<>><<<>><>>>><<>><><<<>><<<<>>>><>>><>><<<<>>>><<<>>>><>><<><<<>><<<<>>><<<>>><>>>><>><>><<<<>>><>>>><<>>>><<<>><<<>>>><<<<><<<><><<<<>><<>>><<>><<>>>><<>>>><<<<>>><<<>><<>>>><<<<><<<>>><<<>>>><<<<>><<<>><<<<>>><<>>><>>>><<<<>><<>>>><<<<>>>><<>><<<<>>>><><<<<>><<<>><<<<>>><<<<><<<<>>>><<<>><<>>>><<<<>><<>>><<>><<>>>><<<<>><<>><<>>>><<><<<>><<>>>><<>><<>>>><<<>><>>>><<>><<<>>>><<>>>><>><<>><<<>>>><<<<>><>>>><<<>><><<<<>>><<<<><<>>>><<<<>><<<<>><<<<>>><>>><<<>>>><<<<><<<<>>><<<>>>><<>><><<<<>>>><<<<>>><<<>>>><<>>>><<>><<<<>><<<<><<<<>>>><<<>>>><<<>>><>>><<<><<<>><<>>><>><<<>>>><<>><>>><<<>>><<<>>><<<>>>><>>><<<>>>><>>>><<<>>><<<<>>><<<>><<>><<<<>><<<<><<<<>><<<<><<<<>>>><<>>><<<>><<>><<<>><<>>>><>><<<<>><<<>>>><>><>>>><<>>><<>><<<<>>>><<><<<>><<<<><>>><<<<>>><>><<<>>><>><>><>><<<>><>>>><<<>>>><<<>>>><<<>><<<<>><<<><<>>><<>>>><>>>><<>>>><<<<>>><<<<><>>><<<<><<>>><<<>>>><<<><<<<>><<<>>>><<<><<<<>><<><<<<>><<<<>><<<>><><><<<>>><><<<>><<<<>><<><<>>><<<>>><<<>><<><<<>>>><<<>><<>>>><<<>>>><>><<<>>><<<<>><><<>>><<<<>>>><><<<<>><<<>><<<>>><<<>><<<<><<><<<><<<>><<<<>>>><<<<>>>><<<<>>>><<>>><<<<>>><<<<>>>><<<><<>><<<<>>>><<>><<>>><<>>>><<>><<>><><<><<><<<<>><>><<><>>><>>><<<><<<>>>><<>>>><<>>><<<>>><<<<>><>>>><<>>>><<><<<<>><<<<>><><<<>><>>>><<><>>>><<<>>>><><>><<><<><><<<>>><<<<>>><<>><<<>>>><<<<>>><<><>>><><<>>><<<><<><<<>>>><<<<>>><<<>><<<<>><<><<<>><<<<><<<><<<<>>><<<<>>><<<>>>><<><<<>>><>>><<>>><><<>>><<<<><<>><<>>><>>><<<<>>><<<<><<>>>><<>>><<>><<<<><>>>><<<>>>><>><<>>>><<<<>>><>><>>><<<>>>><><<<<>><<<<>>>><<<>>><>>>><<>>><><<<<><>>>><<>>><<<<><<<>>>><<<>>><>>>><><>>><<>><>><>><<<>><<<<>><<<><<>>>><<<>>><><<<>><>><<<<>><<>><<<<><<<<>><<<>>>><<<><<<<>>>><<>><<><<<>><>><<<>>>><<>>><<<<><><>>>><>><<<>><<<<><>>><<>>><><>>><<>>>><><<<>>>><<<>>><<<>><>><<>>>><><>><<<<>>>><<<><<<>>><<><<<<><<>>>><<>>>><<<>>>><>>>><<<<>>>><<<>><<<<>><<><<<<>>><<<>>>><<<><<<>>>><<<<>>>><><>>>><<><<<<><>>>><>>>><<<>>><<>>>><<<>>><<<>><<>>>><<>><><<>><<>>><><>>>><>>><<<<>>><<<<>><<<<>>>><<>><<<<>><<<<><<<<>>>><><<><<>>>><<<>><<<<><<<>>>><<<>>><<><<>><<<><<<>>>><><><<<<><><>>>><<>>>><<>><<<<><<<>>><<<><>>><<<<>>>><<<<>>>><<>>><<<<>><<<<>>><<>><<>>><<>>>><>>>><<>>>><>>>><<>>>><<<>><>>><<><<<>>><>><<>><<>>><>>>><<><<>>>><>><<<>>><<>>>><<<<>>><><<>><<>><<<><<<<>>>><<>>>><>><<<>><<<<>><<<<>>><<>>>><<<<><<>><<<><><<>>>><<>>>><<<>>><<<<>>>><<<>>>><<>>><<<<>>><>><<<<>>><<<>>><<>>>><>>>><<<><<>><>><<<<><>>>><>><<<>><>><>>><<<><>>><<<<>><<>>>><>>>><<>>>><<>><<<<>>>><>><<<>>><>>><<>>>><<>>><<<<>>>><<<><<<<>><<<>>>><<<><<<>><<<<>><<<>>><<>>>><><<<>><<<>><<<><<<<>>><<<>>>><<<<>><<>><<<>>><<<<><<<><><<<<>><<<<>>>><<><<<>><<>>>><<>>>><>>>><<>><<<><<>>>><<>><<<>>><<<>>>><>>><>><<<>>>><<><<>>><<<<>>>><<<><<<>><>><<><<<<><<<>>>><<<>>>><<<<>>>><<>><<>><<<<>><>><<>><<>>><<<<>><<<<><<<<>>>><<<>>>><<><<>>>><<<>>><>><<>>><<<<>><<<>>>><<<<>>>><<<<>>>><>>>><><><<<<><<>>><>><<>>><>><<<>>>><<>><<>>><<<<>><<><<>><<<<>><<<<><<<<>><<<<>><<<>><<<<>>><>>>><<>>><>>><<>>>><<>><<<>>><<<>>><<<>><>><<<<>>>><>><>>><<>>>><<>>>><<<>>>><<<<>>>><<<><<<>>>><>><<<>>>><<><<<><>><<<<>>>><<<>>><<<>>>><<><<>>>><<<<>>")
