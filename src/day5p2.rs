use super::day5::*;

pub fn main() {
  let mut map = [[0; 1000]; 1000];
  for line in input() {
    draw(line, &mut map);
  }
  println!("{}", count(&map));
}
