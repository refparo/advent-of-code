def bisect(x: int, arr: list[int], lo: int = -1, hi: int | None = None, left: bool = True):
  """
  when left=True, returns i where arr[i] <= x < arr[i + 1];
  when left=False, returns i where arr[i - 1] < x <= arr[i]
  """
  if hi == None: hi = len(arr)
  while hi - lo > 1:
    mid = (lo + hi) // 2
    if arr[mid] < x:
      lo = mid
    elif arr[mid] > x:
      hi = mid
    else:
      return mid
  return lo if left else hi

def insert_interval(intervals: list[int], lo: int, hi: int):
  """
  insert the interval [lo, hi) into
  the union of intervals [i0, i1), [i2, i3), ...
  """
  if len(intervals) == 0:
    return [lo, hi]
  lo_idx = bisect(lo, intervals, left=False) - 1
  hi_idx = bisect(hi, intervals, lo=lo_idx)
  insertion: list[int] = []
  match (lo_idx % 2, hi_idx % 2):
    case (0, 0): insertion = []
    case (0, 1): insertion = [hi]
    case (1, 0): insertion = [lo]
    case (1, 1): insertion = [lo, hi]
    case _: raise Exception()
  return intervals[:lo_idx + 1] + insertion + intervals[hi_idx + 1:]

def covered_area(sensors: dict[tuple[int, int], tuple[int, int]], y: int):
  intervals: list[int] = []
  for (x0, y0), (x1, y1) in sensors.items():
    radius = abs(x1 - x0) + abs(y1 - y0)
    x_radius = radius - abs(y - y0)
    if x_radius < 0: continue
    xmin, xmax = x0 - x_radius, x0 + x_radius
    intervals = insert_interval(intervals, xmin, xmax + 1)
  return intervals

def solve(y0: int, input: str):
  sensors: dict[tuple[int, int], tuple[int, int]] = {}
  for line in input.strip().splitlines():
    words = line.split()
    sensors[(int(words[2][2:-1]), int(words[3][2:-1]))] = \
      (int(words[-2][2:-1]), int(words[-1][2:]))

  intervals = covered_area(sensors, y0)
  print(sum(
    hi - lo for (lo, hi)
    in zip(intervals[0::2], intervals[1::2])
  ) - sum(
    1 for (xb, yb)
    in set(sensors.values())
    if yb == y0 and bisect(xb, intervals) % 2 == 0
  ), end=" ")

  for y in range(y0 * 2 + 1):
    intervals = covered_area(sensors, y)
    if intervals[1] <= y0 * 2:
      print(intervals[1] * 4000000 + y)
      break

solve(10, """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""")

solve(2000000, """
Sensor at x=3890859, y=2762958: closest beacon is at x=4037927, y=2985317
Sensor at x=671793, y=1531646: closest beacon is at x=351996, y=1184837
Sensor at x=3699203, y=3052069: closest beacon is at x=4037927, y=2985317
Sensor at x=3969720, y=629205: closest beacon is at x=4285415, y=81270
Sensor at x=41343, y=57178: closest beacon is at x=351996, y=1184837
Sensor at x=2135702, y=1658955: closest beacon is at x=1295288, y=2000000
Sensor at x=24022, y=1500343: closest beacon is at x=351996, y=1184837
Sensor at x=3040604, y=3457552: closest beacon is at x=2994959, y=4070511
Sensor at x=357905, y=3997215: closest beacon is at x=-101509, y=3502675
Sensor at x=117943, y=3670308: closest beacon is at x=-101509, y=3502675
Sensor at x=841852, y=702520: closest beacon is at x=351996, y=1184837
Sensor at x=3425318, y=3984088: closest beacon is at x=2994959, y=4070511
Sensor at x=3825628, y=3589947: closest beacon is at x=4299658, y=3299020
Sensor at x=2745170, y=139176: closest beacon is at x=4285415, y=81270
Sensor at x=878421, y=2039332: closest beacon is at x=1295288, y=2000000
Sensor at x=1736736, y=811875: closest beacon is at x=1295288, y=2000000
Sensor at x=180028, y=2627284: closest beacon is at x=-101509, y=3502675
Sensor at x=3957016, y=2468479: closest beacon is at x=3640739, y=2511853
Sensor at x=3227780, y=2760865: closest beacon is at x=3640739, y=2511853
Sensor at x=1083678, y=2357766: closest beacon is at x=1295288, y=2000000
Sensor at x=1336681, y=2182469: closest beacon is at x=1295288, y=2000000
Sensor at x=3332913, y=1556848: closest beacon is at x=3640739, y=2511853
Sensor at x=3663725, y=2525708: closest beacon is at x=3640739, y=2511853
Sensor at x=2570900, y=2419316: closest beacon is at x=3640739, y=2511853
Sensor at x=1879148, y=3584980: closest beacon is at x=2994959, y=4070511
Sensor at x=3949871, y=2889309: closest beacon is at x=4037927, y=2985317
""")
