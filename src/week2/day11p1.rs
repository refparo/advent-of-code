use super::day11::*;

pub fn main() {
  let mut map = input();
  println!("{}", (0..100).map(|_| step(&mut map)).sum::<usize>());
}
