from copy import deepcopy
from functools import reduce
from typing import Callable

class Monkey:
  WORRY_REDUCTION: Callable[[int], int] = lambda x: x // 3

  items: list[int]
  operation: Callable[[int], int]
  test: int
  if_true: int
  if_false: int
  business: int

  def __init__(self, input: str):
    lines = input.splitlines()
    self.items = [int(x) for x in lines[1].split(None, 2)[2].split(",")]
    match lines[2].split()[4:]:
      case ["+", x]:
        x = int(x)
        self.operation = lambda old: old + x
      case ["*", "old"]:
        self.operation = lambda old: old * old
      case ["*", x]:
        x = int(x)
        self.operation = lambda old: old * x
      case _: raise Exception()
    self.test = int(lines[3].split()[3])
    self.if_true = int(lines[4].split()[5])
    self.if_false = int(lines[5].split()[5])
    self.business = 0

  def action(self, monkeys: list["Monkey"]):
    for item in self.items:
      item = Monkey.WORRY_REDUCTION(self.operation(item))
      monkeys[
        self.if_true if item % self.test == 0 else self.if_false
      ].items.append(item)
    self.business += len(self.items)
    self.items.clear()

def part_solve(monkeys: list[Monkey], turn: int):
  for _ in range(turn):
    for monkey in monkeys:
      monkey.action(monkeys)
  [a, b] = sorted((it.business for it in monkeys), reverse=True)[:2]
  return a * b

def solve(input: str):
  monkeys = [Monkey(s) for s in input.strip().split("\n\n")]
  s1 = part_solve(deepcopy(monkeys), 20)
  lcm = reduce(lambda x, y: x * y, (m.test for m in monkeys), 1)
  Monkey.WORRY_REDUCTION = lambda x: x % lcm
  s2 = part_solve(monkeys, 10000)
  print(s1, s2)

solve("""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""")

solve("""
Monkey 0:
  Starting items: 85, 77, 77
  Operation: new = old * 7
  Test: divisible by 19
    If true: throw to monkey 6
    If false: throw to monkey 7

Monkey 1:
  Starting items: 80, 99
  Operation: new = old * 11
  Test: divisible by 3
    If true: throw to monkey 3
    If false: throw to monkey 5

Monkey 2:
  Starting items: 74, 60, 74, 63, 86, 92, 80
  Operation: new = old + 8
  Test: divisible by 13
    If true: throw to monkey 0
    If false: throw to monkey 6

Monkey 3:
  Starting items: 71, 58, 93, 65, 80, 68, 54, 71
  Operation: new = old + 7
  Test: divisible by 7
    If true: throw to monkey 2
    If false: throw to monkey 4

Monkey 4:
  Starting items: 97, 56, 79, 65, 58
  Operation: new = old + 5
  Test: divisible by 5
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 5:
  Starting items: 77
  Operation: new = old + 4
  Test: divisible by 11
    If true: throw to monkey 4
    If false: throw to monkey 3

Monkey 6:
  Starting items: 99, 90, 84, 50
  Operation: new = old * old
  Test: divisible by 17
    If true: throw to monkey 7
    If false: throw to monkey 1

Monkey 7:
  Starting items: 50, 66, 61, 92, 64, 78
  Operation: new = old + 3
  Test: divisible by 2
    If true: throw to monkey 5
    If false: throw to monkey 1
""")
