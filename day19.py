from dataclasses import dataclass, field
from functools import reduce
from typing import NamedTuple

@dataclass
class Blueprint:
  ore_robot: int
  clay_robot: int
  obsidian_robot_ore: int
  obsidian_robot_clay: int
  geode_robot_ore: int
  geode_robot_obsidian: int
  
  max_ore: int = field(init=False)
  min_ore: int = field(init=False)

  def __post_init__(self):
    self.max_ore = max(
      self.ore_robot,
      self.clay_robot,
      self.obsidian_robot_ore,
      self.geode_robot_ore
    )
  
  @staticmethod
  def parse(line: str):
    words = line.split()
    return Blueprint(
      ore_robot=int(words[6]),
      clay_robot=int(words[12]),
      obsidian_robot_ore=int(words[18]),
      obsidian_robot_clay=int(words[21]),
      geode_robot_ore=int(words[27]),
      geode_robot_obsidian=int(words[30])
    )

class Factory(NamedTuple):
  ore_robot: int = 1
  clay_robot: int = 0
  obsidian_robot: int = 0
  geode_robot: int = 0
  
  ore: int = 0
  clay: int = 0
  obsidian: int = 0
  geode: int = 0
  
  def tick(self, blueprint: Blueprint):
    if self.obsidian >= blueprint.geode_robot_obsidian \
    and self.ore >= blueprint.geode_robot_ore:
      yield Factory(
        self.ore_robot,
        self.clay_robot,
        self.obsidian_robot,
        self.geode_robot + 1,
        
        self.ore + self.ore_robot - blueprint.geode_robot_ore,
        self.clay + self.clay_robot,
        self.obsidian + self.obsidian_robot - blueprint.geode_robot_obsidian,
        self.geode + self.geode_robot
      )

    if self.obsidian_robot < blueprint.geode_robot_obsidian \
    and self.clay >= blueprint.obsidian_robot_clay \
    and self.ore >= blueprint.obsidian_robot_ore:
      yield Factory(
        self.ore_robot,
        self.clay_robot,
        self.obsidian_robot + 1,
        self.geode_robot,
        
        self.ore + self.ore_robot - blueprint.obsidian_robot_ore,
        self.clay + self.clay_robot - blueprint.obsidian_robot_clay,
        self.obsidian + self.obsidian_robot,
        self.geode + self.geode_robot
      )
    
    if self.clay_robot < blueprint.obsidian_robot_clay \
    and self.ore >= blueprint.clay_robot:
      yield Factory(
        self.ore_robot,
        self.clay_robot + 1,
        self.obsidian_robot,
        self.geode_robot,
        
        self.ore + self.ore_robot - blueprint.clay_robot,
        self.clay + self.clay_robot,
        self.obsidian + self.obsidian_robot,
        self.geode + self.geode_robot
      )
    
    if self.ore_robot < blueprint.max_ore \
    and self.ore >= blueprint.ore_robot:
      yield Factory(
        self.ore_robot + 1,
        self.clay_robot,
        self.obsidian_robot,
        self.geode_robot,
        
        self.ore + self.ore_robot - blueprint.ore_robot,
        self.clay + self.clay_robot,
        self.obsidian + self.obsidian_robot,
        self.geode + self.geode_robot
      )
    
    if self.ore < blueprint.max_ore:
      yield Factory(
        self.ore_robot,
        self.clay_robot,
        self.obsidian_robot,
        self.geode_robot,
        
        self.ore + self.ore_robot,
        self.clay + self.clay_robot,
        self.obsidian + self.obsidian_robot,
        self.geode + self.geode_robot
      )

def max_geode(blueprint: Blueprint, time: int):
  history = [Factory().tick(blueprint)]
  best = [0] * (time + 1)
  while len(history) > 0:
    try:
      factory = next(history[-1])
    except StopIteration:
      history.pop()
      continue
    if factory.geode > best[len(history)]:
      best[len(history)] = factory.geode
    if len(history) == time: continue
    if factory.geode < best[len(history)]: continue
    history.append(factory.tick(blueprint))
  return best[time]

def solve(input: str):
  blueprints = [Blueprint.parse(line) for line in input.strip().splitlines()]
  print(
    sum(
      i * max_geode(blueprint, 24)
      for i, blueprint in enumerate(blueprints, 1)
    ),
    reduce(
      lambda a, b: a * b,
      (max_geode(blueprint, 32) for blueprint in blueprints[:3]),
      1
    )
  )

solve("""
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""")

solve("""
Blueprint 1: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 15 clay. Each geode robot costs 2 ore and 20 obsidian.
Blueprint 2: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 20 clay. Each geode robot costs 2 ore and 8 obsidian.
Blueprint 3: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 8 obsidian.
Blueprint 4: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 15 clay. Each geode robot costs 2 ore and 13 obsidian.
Blueprint 5: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 20 clay. Each geode robot costs 4 ore and 18 obsidian.
Blueprint 6: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 17 clay. Each geode robot costs 2 ore and 13 obsidian.
Blueprint 7: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 12 clay. Each geode robot costs 4 ore and 19 obsidian.
Blueprint 8: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 15 clay. Each geode robot costs 2 ore and 13 obsidian.
Blueprint 9: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 9 clay. Each geode robot costs 2 ore and 9 obsidian.
Blueprint 10: Each ore robot costs 3 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 12 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 11: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 10 clay. Each geode robot costs 2 ore and 13 obsidian.
Blueprint 12: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 6 clay. Each geode robot costs 3 ore and 16 obsidian.
Blueprint 13: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 5 clay. Each geode robot costs 3 ore and 19 obsidian.
Blueprint 14: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 20 clay. Each geode robot costs 4 ore and 16 obsidian.
Blueprint 15: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 8 clay. Each geode robot costs 2 ore and 18 obsidian.
Blueprint 16: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 10 clay. Each geode robot costs 4 ore and 10 obsidian.
Blueprint 17: Each ore robot costs 2 ore. Each clay robot costs 2 ore. Each obsidian robot costs 2 ore and 17 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 18: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 11 clay. Each geode robot costs 3 ore and 14 obsidian.
Blueprint 19: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 13 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 20: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 5 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 21: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 4 ore and 15 obsidian.
Blueprint 22: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 20 clay. Each geode robot costs 2 ore and 15 obsidian.
Blueprint 23: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 5 clay. Each geode robot costs 2 ore and 10 obsidian.
Blueprint 24: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 5 clay. Each geode robot costs 4 ore and 8 obsidian.
Blueprint 25: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 17 clay. Each geode robot costs 3 ore and 10 obsidian.
Blueprint 26: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 6 clay. Each geode robot costs 2 ore and 20 obsidian.
Blueprint 27: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 5 clay. Each geode robot costs 3 ore and 15 obsidian.
Blueprint 28: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 17 clay. Each geode robot costs 4 ore and 20 obsidian.
Blueprint 29: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 14 clay. Each geode robot costs 3 ore and 17 obsidian.
Blueprint 30: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 9 clay. Each geode robot costs 3 ore and 9 obsidian.
""")
