use super::day9::*;

pub fn main() {
  let map = input();
  println!("{}", low_points(&map)
    .map(|(i, j)| map[i][j] + 1)
    .sum::<u32>());
}
