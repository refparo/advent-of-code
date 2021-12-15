use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Map = Vec<u32>;

pub fn input() -> (Map, usize) {
  let file = File::open("input/day15.txt").unwrap();
  let mut lines = BufReader::new(file).lines().peekable();
  let width = lines.peek().unwrap().as_ref().unwrap().len();
  let mut map = Vec::with_capacity(width * width);
  for l in lines {
    for c in l.unwrap().chars() {
      map.push(c.to_digit(10).unwrap());
    }
  }
  (map, width)
}
