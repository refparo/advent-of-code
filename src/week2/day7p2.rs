use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day7.txt").unwrap();
  let nums = BufReader::new(file).lines()
    .next().unwrap().unwrap()
    .split(',').map(|x| x.parse::<i32>().unwrap()).collect::<Vec<_>>();
  let avg = (
    (&nums).into_iter().sum::<i32>() as f64 /
    nums.len() as f64 - 0.5
  ).round() as i32;
  println!("{}", nums.into_iter()
    .map(|x| (avg - x).abs() * (1 + (avg - x).abs()) / 2)
    .sum::<i32>());
}
