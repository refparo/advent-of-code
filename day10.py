def vm(instr: list[str]):
  reg = 1
  for line in instr:
    match line.split():
      case ["addx", x]:
        yield reg
        yield reg
        reg += int(x)
      case ["noop"]:
        yield reg
      case _: raise Exception()

def solve(input: str):
  checksum = 0
  for t, reg in enumerate(vm(input.strip().splitlines())):
    if (t - 19) % 40 == 0 and t < 220: checksum += (t + 1) * reg
    print(
      "#" if abs((t % 40) - reg) <= 1 else " ",
      end="\n" if (t % 40) == 39 else ""
    )
  print(checksum)

solve("""
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""")

solve("""
addx 1
noop
addx 5
addx -1
noop
addx 5
noop
addx -2
addx 8
addx -1
addx 7
noop
addx -1
addx 4
noop
addx 1
noop
noop
addx 6
addx -1
addx 3
addx 2
addx -5
addx -27
addx -3
addx 2
noop
addx 3
addx 2
addx 5
addx 2
addx 3
noop
addx 5
noop
noop
addx -2
addx 2
noop
addx -13
addx 23
noop
noop
addx -9
addx -18
addx 30
noop
addx -34
addx 3
addx -2
noop
addx 1
addx 6
noop
addx 28
addx -25
addx 5
addx 5
addx -11
addx 9
addx 4
noop
addx -26
addx 34
noop
addx -2
noop
noop
addx 4
addx -34
noop
addx 11
addx -7
addx 7
addx -9
addx 5
addx 5
addx 2
addx 1
noop
noop
noop
addx 22
addx -17
addx 2
noop
addx -19
addx 29
noop
addx -2
noop
addx 3
noop
noop
addx -36
addx 7
noop
noop
addx 3
addx -2
addx 2
addx 5
addx 2
addx 3
noop
addx 2
addx 11
addx -10
addx 2
addx 7
noop
addx -2
addx 5
addx 2
addx -36
addx 1
addx -1
addx 3
addx 4
addx -1
addx 5
noop
noop
noop
noop
noop
addx 3
addx 5
addx 15
addx -13
addx 6
addx -3
addx -1
addx 9
addx -1
addx 5
noop
addx 1
noop
noop
noop
noop
""")
