use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day7.txt").unwrap();
  let mut nums = BufReader::new(file).lines()
    .next().unwrap().unwrap()
    .split(',').map(|x| x.parse::<i32>().unwrap()).collect::<Vec<_>>();
  // f(x) = sum(abs(x - num))
  // minimum value at x = median(num)
  nums.sort_unstable();
  let median = nums[nums.len() / 2];
  println!("{}", nums.into_iter().map(|num| (median - num).abs()).sum::<i32>());
}
