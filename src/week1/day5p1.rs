use super::day5::*;

pub fn main() {
  let mut map = [[0; 1000]; 1000];
  for line@((x1, y1), (x2, y2)) in input() {
    if x1 == x2 || y1 == y2 {
      draw(line, &mut map);
    }
  }
  println!("{}", count(&map));
}
