from itertools import count
import numpy as np

step = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]

def solve(input: str):
  lines = input.strip().splitlines()
  xlen, ylen = len(lines[0]) - 2, len(lines) - 2
  start = (0, -1)
  end = (xlen - 1, ylen)
  right = np.zeros((xlen, ylen), np.bool_)
  left = np.zeros((xlen, ylen), np.bool_)
  up = np.zeros((xlen, ylen), np.bool_)
  down = np.zeros((xlen, ylen), np.bool_)
  for y, line in enumerate(lines[1:-1]):
    for x, c in enumerate(line[1:-1]):
      match c:
        case '.': pass
        case '>': right[x, y] = True
        case '<': left[x, y] = True
        case '^': up[x, y] = True
        case 'v': down[x, y] = True
        case _: raise Exception()
  pos = [start]
  def trip(start: tuple[int, int], end: tuple[int, int]) -> int: # type: ignore
    nonlocal right, left, up, down, pos
    for t in count(1):
      right = np.roll(right, 1, axis=0) # type: ignore
      left = np.roll(left, -1, axis=0) # type: ignore
      up = np.roll(up, -1, axis=1) # type: ignore
      down = np.roll(down, 1, axis=1) # type: ignore
      newpos: list[tuple[int, int]] = []
      for (x, y) in {(x + dx, y + dy) for (x, y) in pos for (dx, dy) in step}:
        if (x, y) == end:
          pos = [end]
          return t
        if (x, y) == start:
          newpos.append((x, y))
          continue
        if 0 <= x < xlen and 0 <= y < ylen and not (
          right[x, y] or left[x, y] or up[x, y] or down[x, y]
        ):
          newpos.append((x, y))
      pos = newpos
  t1 = trip(start, end)
  t2 = trip(end, start)
  t3 = trip(start, end)
  print(t1, t1 + t2 + t3)

solve("""
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""")

solve("""
#.######################################################################################################################################################
#>v<<.^vvv^vv.^^>>v<>><v^<<.>^>v>v<v^vvvvvv^><^<vv<^^^v<vv>vvv.^v>.<>>v^v><<>^<<^vv<<>><<v<v<^v<..^>>vv^><<<v<^^><<<>>>vvv^.^.v>.^v^^.vv>^vv^>^^^><v<<<#
#.<<v^><<.<>>>>^.<^<^^<>>^.^^.^v<vvv>>vv<^>.>>^^<<<^^>><^><<<v^>v.^^<.<<^v^>^^>.^.v^>.><<vv^>><>^....^<vv^><<^>v<v<^vvv<v<<><^vv<^>v^^^^^^^.^vv<^^<vvv<#
#<>.v^.v<^><><v^^>>^><.v>^v^vv><><>>^>^v<^>>v^>^vvv^v..>vv>.^vv^<^.<.<v>>^<><v>^>^v..^>^><>vvv<v>^.>>^^<v^v>^<^vv.>.^v><v>v^>.^v<v>.<<vvv><^v^<^<^<vv<>#
#>v..v^<^^v<><^^>vv>v^^^<^.^<<><^^^v>^<^v<<^>^<<.^><<^>>v^.v.><>>^<<><^^>>v>.^<^<vv><<>..>>v^^^>v>^<vv>.^>^<.^^v<>v>^.^>^^>.^v^>>^v>>>^<<^.^>><>v^>v>v.#
#>^^^^^v^>>>^^v^v^v>v^v<v^.><<.^..v<^<^<^><<><<<>>v<<>><<^v^^>v>v<>.<vv>^<<<><.v<v<>>v^v<>>^v><.v>><<v><v<vv<<^^<><.^>v>^<^<^>^^.<.v>v^>>>><<<^v.vv<.<>#
#>vv<vv^v<.<<v><<<^v>v<><vv<<vv<<.^.v>>v>.>v<^<<>v>>vv>..>v<^.v<.^<.>.<<<>>>^v>.^>>>>><<<^>..>>>^<^<>^>><>^><><v>v<<<v^.vvvv<v>>vv^>>>^.v^<>^><.<v>>v>>#
#>>v.>><v^>v^v.<^.<vvv<<<v<>.^^v<<^^>>^^v^^.^.<>^vv^>>v<>^>v^.vv^v>.v^<>>v<<v<^>^vv^^v^><>v>.^<v<v<.^>>vvv>v^<^vv^<v^<<>^<v<>v<<v<<>v^v><>^vv^<<<^v>^>>#
#<^<^>><<.<<.><<v>vv>v^v<<>..v<^>v^<.vv><v^<<<.v>v>>><<^.<v^vvv^<^v<<^^^^<v<<.<<^><v.<>>^><v>..<><vvv<.<>><.v>.v><<>vv<>.<<v.>><>>v<v^>^>>..>.<<^>^>^.>#
#<v.>v>v<>>v^v>^v<^vv>^^>^vv>v<^^vv><^.<v<^<v>^>^v<v.<^<>^>>>vvvv<v>>^^<v.^v<^^<.<<<><v^<>^^<vvv><<>...^<><>^>vvv^^v..v..v^><^<>^>vv><v<^^vv^vvv>v^<v><#
#<^^^^.>v>><<>v<vv<^<<^>v..vv^vvv>>>v<<^vv^^><^>^>^v.<<^v^^><vv>.>v..v.^v><^<^>>^>vv<<v.v>.<.>^.>>>^>>^^v^>^<.<><v>v^.^..<>.>^<^^<v.^v>^^^<<^v>>.>vv<v>#
#>^^v>v.<v<<v..>><>..^v><>.^<v.>vv<>v^^>v.^v<<<vv>>v.^>><<^<v><v^.>>>^v>^>>v<<...<^^^vv.v^><<<>^^v<v^>v<v>.vv^vv.>>v<>><>v><vv>^>>v^..vv>v>^^>vvv>.>^v<#
#<v>^^.<.^vv^<>^vv<<<<<vv^<^^<>v>^vv<>v<<>vv^<<v><<.^^..>.^>vv<^<>>^.<<<<<>.v>v><>.>v>v^<>^>vvv>.<^v^.>^<<v<^vvv^>v><<v^>.^><^><>v.^^<><vv<>.v..^<<v^>>#
#<>^.>.><><v^<v>v>^<<>^v..<.<><>>^.vv>v.vv.>><>v^>.^><.<v.>v..^^v.^v^>^<^^<>>>v<^>>v<^<v^^^v<^v.vv<v^.><^^v^>^^^<.>.<v<.<v>^.><^^<v^<<^^v<.>>v>.vvv>v>>#
#<v><v.^^<>v>.>^^^^>v<<v..v>><>v^.>^^<^>v<>v^v<v^<><^<>v>v^.<.^v^<^<>v^^<<^v><^.>^.v><><>>^v^v><.>v><<>v>v^.vvv><>^>>v^<<^v>^vv><><.^^>>vv^^v><^..>^v<>#
#>v><^<vv^v>v><>v^<<><<^>v^v<^<^<v>><v^vv<<.vv<^v.><<<v.v.^<v<v.^^>><>^vv>v<v^>v^.<<><^<<.<vv<^.^>^^vv<^vv^..<^>^^<^^vvvv<><^^^<v<vv<v^>^v<^v><^^<..<v>#
#>v^<<><<<^v.vvv>v<<v>>.^>^<^><..>>>^v.v.<<v<>>^^..><<v>vv^^<v<<^<>^v<^<<^.v>^<^>vv.>>>^>^^.<^<v<<^^v^^<><.>^.<><vv^<^>^>>^^vv^<^^^<^>^.v^<.<^^<.>v>v>>#
#>^<v>v^<^>>..v<.><<<^><^v>vv<>^^v<v^vv><<<><^v<^.v<^>v<v<^<v>v>^v^^>>^<<^.<<v<vvv><^>v>^<>v>v^^>.<vv<<>>^^<>vv>^v^.><^^^vv>v<<<<v^v<vv><.<v<^v>>^v>v<>#
#<vv^>^^<v>^v>>.^.<<^<^^.v>>vv>^<><><>>^>>>vv<.v<^<<<vvv.>v<>>^>>v<>>..>^v^>^>^v<<>v^v^.^>^v^^v>.><v<<.v<v>vv>>.<<v.v.^<>><>vv>^^>><^^.<>>>vv<<>^>><<<.#
#<^<^^.>>>^<>^v<^v<<>v^<>^vv<^^v<v<<^^.><<vv>v^<^^<>^^^v<v>^.^^<<^v<v^.^>>>><v>><>>>><v<^^<v>v^v>^>v>v^^^<>v><v><.>><>^vvvvv>vv<<v^^<v^v>v.^v<vv<^.^^v<#
#..>^>>^^^^v<>>^><^^v>^^>v.><>><vv<><^.<><^v.^vv<><v>v^<<v>v<vv<><>v^.^<<<vv>>^^<<>^.v<^.v^^<>>>^v<.>^..^^^<<<>..v<><v<>v<>>..<v><>^^>>.<>v<<>v>.<v^vv.#
######################################################################################################################################################.#
""")
