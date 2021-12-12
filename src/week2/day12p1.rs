use super::day12::*;

pub fn main() {
  let graph = input();
  println!("{}", search::<true>(&graph, &mut vec!["start"]));
}
