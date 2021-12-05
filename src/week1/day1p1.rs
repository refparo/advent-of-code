use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day1.txt").unwrap();
  let mut inc = 0;
  BufReader::new(file)
    .lines()
    .map(|x| x.unwrap().parse::<u32>().unwrap())
    .reduce(|a, b| {
      if a < b { inc += 1; }
      b
    });
  println!("{}", inc);
}
