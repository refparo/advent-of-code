use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day7.txt").unwrap();
  let nums = BufReader::new(file).lines()
    .next().unwrap().unwrap()
    .split(',').map(|x| x.parse::<i32>().unwrap()).collect::<Vec<_>>();
  // f(x) = sum((1 + abs(x - num)) * abs(x - num) / 2)
  // minimum value at x = round(avg(num - 1/2)) = floor(avg(num))
  let avg = (&nums).into_iter().sum::<i32>() / nums.len() as i32;
  println!("{}", nums.into_iter()
    .map(|num| (1 + (avg - num).abs()) * (avg - num).abs() / 2)
    .sum::<i32>());
}
