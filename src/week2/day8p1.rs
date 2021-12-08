use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day8.txt").unwrap();
  println!("{}", BufReader::new(file).lines()
    .map(|line| line.unwrap().split_ascii_whitespace().skip(11)
      .filter(|s| matches!(s.len(), 2 | 3 | 4 | 7)).count())
    .sum::<usize>());
}
