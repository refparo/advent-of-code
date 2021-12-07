use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day7.txt").unwrap();
  let mut nums = BufReader::new(file).lines()
    .next().unwrap().unwrap()
    .split(',').map(|x| x.parse::<i32>().unwrap()).collect::<Vec<_>>();
  nums.sort_unstable();
  let mid = nums[nums.len() / 2];
  println!("{}", nums.into_iter().map(|x| (x - mid).abs()).sum::<i32>());
}
