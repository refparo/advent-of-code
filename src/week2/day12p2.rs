use super::day12::*;

pub fn main() {
  let graph = input();
  println!("{}", search::<false>(&graph, &mut vec!["start"]));
}
