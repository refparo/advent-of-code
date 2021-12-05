use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day2.txt").unwrap();
  let mut a = 0;
  let mut x = 0;
  let mut y = 0;
  for line in BufReader::new(file).lines().map(|x| x.unwrap()) {
    let (instr, num_str) = line.split_once(" ").unwrap();
    let num = num_str.parse::<i32>().unwrap();
    match instr {
      "forward" => { x += num; y += a * num; }
      "down" => { a += num; }
      "up" => { a -= num; }
      _ => { panic!(); }
    }
  }
  println!("{}", x * y);
}
