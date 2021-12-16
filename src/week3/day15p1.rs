// Fortunately, the input doesn't require walking backwards.

use super::day15::*;

type DistMap = Vec<u32>;

fn search(map: &Map, dist_map: &mut DistMap, width: usize,
  (i, j): (usize, usize)) -> u32 {
  let pos = i * width + j;
  if dist_map[pos] > 0 { return dist_map[pos]; }
  let mut min = u32::MAX;
  if i < width - 1 {
    min = min.min(search(map, dist_map, width, (i + 1, j)));
  }
  if j < width - 1 {
    min = min.min(search(map, dist_map, width, (i, j + 1)));
  }
  min += map[pos];
  dist_map[pos] = min;
  min
}

pub fn main() {
  let (map, width) = input();
  let mut dist_map = vec![0; map.len()];
  let target = map.len() - 1;
  dist_map[target] = map[target];
  println!("{}", search(&map, &mut dist_map, width, (0, 0)) - map[0]);
}
