import numpy as np
from numpy.typing import NDArray

def parse(input: str):
  import re
  graph: dict[str, tuple[int, list[str]]] = {}
  regex = re.compile(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
  for line in input.strip().splitlines():
    words = regex.fullmatch(line)
    assert words != None
    key, rate, tunnels = words.groups()
    graph[key] = (int(rate), tunnels.split(", "))
  return graph

def floyd_warshall(graph: dict[str, tuple[int, list[str]]]):
  keys = list(graph.keys())
  invkeys = dict((key, i) for i, key in enumerate(keys))
  dist = np.full((len(keys), len(keys)), np.inf)
  for i in range(len(keys)): dist[i, i] = 0
  for i, room in enumerate(keys):
    for other in graph[room][1]:
      dist[i, invkeys[other]] = 1
  for k in range(len(keys)):
    for i in range(len(keys)):
      for j in range(len(keys)):
        if dist[i, j] > dist[i, k] + dist[k, j]:
          dist[i, j] = dist[i, k] + dist[k, j]
  return keys, invkeys, dist

def filter_graph(graph: dict[str, tuple[int, list[str]]]):
  keys, invkeys, dist = floyd_warshall(graph)
  filtered = [invkeys["AA"], *(i for i, key in enumerate(keys) if graph[key][0] != 0)]
  dist = dist[np.ix_(filtered, filtered)]
  rates = list(graph[keys[i]][0] for i in filtered)
  return rates, dist

def search(rates: list[int], dist: NDArray[np.float64], elephant: bool):
  TIMELIMIT = 26 if elephant else 30
  # len(passed) -> list[(pos, time, total, passed, dest)]
  mem: list[list[tuple[int, float, float, list[int], set[int]]]] = \
    [[(0, 0, 0, [], set(range(1, len(rates))))]]
  while True:
    nextlen: list[tuple[int, float, float, list[int], set[int]]] = []
    for pos, time, total, passed, dest in mem[-1]:
      for next in dest:
        nexttime: float = time + dist[pos, next] + 1
        if nexttime >= TIMELIMIT: continue
        nexttotal = total + (TIMELIMIT - nexttime) * rates[next]
        nextpassed = passed + [next]
        nextlen.append((next, nexttime, nexttotal, nextpassed, dest - {next}))
    if len(nextlen) == 0: break
    else: mem.append(nextlen)
  if not elephant:
    return max(value[2] for l in mem for value in l)
  else:
    # here we may first filter out the max total of each different dest set
    # or we can filter them out in the first step (that would be a bit complex)
    # but I'm too lazy to do that
    # after all, 2.5s is already blazingly fast
    maxlen = len(rates) - 1
    return max(
      total1 + total2
      for i in reversed(range(maxlen // 2, len(mem)))
      for j in range(len(mem) // 2, min(i, maxlen - i) + 1)
      for _, _, total1, _, dest1 in mem[i]
      for _, _, total2, passed2, _ in mem[j]
      if dest1.issuperset(passed2)
    )

def solve(input: str):
  rates, dist = filter_graph(parse(input))
  print(search(rates, dist, False), search(rates, dist, True))

solve("""
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""")

solve("""
Valve OQ has flow rate=17; tunnels lead to valves NB, AK, KL
Valve HP has flow rate=0; tunnels lead to valves ZX, KQ
Valve GO has flow rate=0; tunnels lead to valves HR, GW
Valve PD has flow rate=9; tunnels lead to valves XN, EV, QE, MW
Valve NQ has flow rate=0; tunnels lead to valves HX, ZX
Valve DW has flow rate=0; tunnels lead to valves IR, WE
Valve TN has flow rate=24; tunnels lead to valves KL, EI
Valve JJ has flow rate=0; tunnels lead to valves EV, HR
Valve KH has flow rate=0; tunnels lead to valves ZQ, AA
Valve PH has flow rate=0; tunnels lead to valves FN, QE
Valve FD has flow rate=0; tunnels lead to valves SM, HX
Valve SM has flow rate=7; tunnels lead to valves WW, RZ, FD, HO, KQ
Valve PU has flow rate=0; tunnels lead to valves VL, IR
Valve OM has flow rate=0; tunnels lead to valves CM, AA
Valve KX has flow rate=20; tunnel leads to valve PC
Valve IR has flow rate=3; tunnels lead to valves PU, CM, WW, DW, AF
Valve XG has flow rate=0; tunnels lead to valves RX, OF
Valve QE has flow rate=0; tunnels lead to valves PH, PD
Valve GW has flow rate=0; tunnels lead to valves JQ, GO
Valve HO has flow rate=0; tunnels lead to valves SM, TY
Valve WU has flow rate=0; tunnels lead to valves SG, RZ
Valve MS has flow rate=0; tunnels lead to valves UE, OF
Valve JS has flow rate=0; tunnels lead to valves DO, ZX
Valve YQ has flow rate=0; tunnels lead to valves BC, SG
Valve EJ has flow rate=0; tunnels lead to valves AA, LR
Valve EI has flow rate=0; tunnels lead to valves BV, TN
Valve NC has flow rate=0; tunnels lead to valves TS, BC
Valve AF has flow rate=0; tunnels lead to valves IR, HX
Valve OX has flow rate=0; tunnels lead to valves HR, BV
Valve BF has flow rate=0; tunnels lead to valves JQ, SY
Valve CA has flow rate=0; tunnels lead to valves YD, HX
Valve KQ has flow rate=0; tunnels lead to valves HP, SM
Valve NB has flow rate=0; tunnels lead to valves OQ, OF
Valve SY has flow rate=0; tunnels lead to valves BF, BV
Valve AA has flow rate=0; tunnels lead to valves KH, EJ, OM, TY, DO
Valve BC has flow rate=11; tunnels lead to valves WE, RX, YQ, LR, NC
Valve HR has flow rate=14; tunnels lead to valves OX, GO, JJ
Valve WE has flow rate=0; tunnels lead to valves DW, BC
Valve MW has flow rate=0; tunnels lead to valves JQ, PD
Valve DO has flow rate=0; tunnels lead to valves JS, AA
Valve PC has flow rate=0; tunnels lead to valves AK, KX
Valve YD has flow rate=0; tunnels lead to valves CA, OF
Valve RX has flow rate=0; tunnels lead to valves XG, BC
Valve CM has flow rate=0; tunnels lead to valves IR, OM
Valve HX has flow rate=6; tunnels lead to valves ZQ, NQ, AF, FD, CA
Valve ZQ has flow rate=0; tunnels lead to valves KH, HX
Valve BV has flow rate=21; tunnels lead to valves SY, OX, EI
Valve AK has flow rate=0; tunnels lead to valves PC, OQ
Valve UE has flow rate=0; tunnels lead to valves MS, JQ
Valve LR has flow rate=0; tunnels lead to valves BC, EJ
Valve JQ has flow rate=8; tunnels lead to valves MW, UE, BF, GW
Valve VL has flow rate=0; tunnels lead to valves PU, ZX
Valve EV has flow rate=0; tunnels lead to valves JJ, PD
Valve TS has flow rate=0; tunnels lead to valves NC, ZX
Valve RZ has flow rate=0; tunnels lead to valves SM, WU
Valve OF has flow rate=13; tunnels lead to valves XG, YD, NB, MS, XN
Valve WW has flow rate=0; tunnels lead to valves SM, IR
Valve TY has flow rate=0; tunnels lead to valves HO, AA
Valve XN has flow rate=0; tunnels lead to valves OF, PD
Valve SG has flow rate=15; tunnels lead to valves WU, YQ
Valve FN has flow rate=25; tunnel leads to valve PH
Valve KL has flow rate=0; tunnels lead to valves TN, OQ
Valve ZX has flow rate=5; tunnels lead to valves JS, HP, VL, NQ, TS
""")
