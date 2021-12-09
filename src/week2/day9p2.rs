use super::day9::*;

fn flood_fill(map: &mut Vec<Vec<u32>>, (i, j): (usize, usize)) -> usize {
  if map[i][j] >= 9 { return 0; }
  map[i][j] = !map[i][j];
  let mut res = 1;
  if j > 0 { res += flood_fill(map, (i, j - 1)); }
  if j < map[i].len() - 1 { res += flood_fill(map, (i, j + 1)); }
  if i > 0 { res += flood_fill(map, (i - 1, j)); }
  if i < map.len() - 1 { res += flood_fill(map, (i + 1, j)); }
  res
}

pub fn main() {
  let mut map = input();
  let mut sizes = low_points(&map)
    .collect::<Vec<_>>().into_iter()
    .map(|pos| flood_fill(&mut map, pos)).collect::<Vec<_>>();
  sizes.sort_unstable();
  println!("{}", sizes.iter().rev().take(3).product::<usize>());
}
