use super::day9::*;

fn flood_fill(map: &mut Vec<Vec<u32>>, pos: (usize, usize)) -> usize {
  use std::collections::VecDeque;
  let mut cue = VecDeque::with_capacity(32);
  cue.push_back(pos);
  let mut res = 0;
  while let Some((i, j)) = cue.pop_front() {
    if map[i][j] >= 9 { continue; }
    res += 1;
    map[i][j] = !map[i][j];
    if j > 0 { cue.push_back((i, j - 1)); }
    if j < map[i].len() - 1 { cue.push_back((i, j + 1)); }
    if i > 0 { cue.push_back((i - 1, j)); }
    if i < map.len() - 1 { cue.push_back((i + 1, j)); }
  }
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
