use super::day11::*;

pub fn main() {
  let mut map = input();
  for i in 1usize.. {
    if step(&mut map) == 100 {
      println!("{}", i);
      break;
    }
  }
}
