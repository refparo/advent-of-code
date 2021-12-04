use std::fs::File;
use std::io::{BufRead, BufReader};
use std::mem::size_of;

pub fn main() {
  let file = File::open("input/day3.txt").unwrap();
  let mut lines = BufReader::new(file).lines().map(|l| l.unwrap()).peekable();
  let width = lines.peek().unwrap().len();
  let nums = lines.map(|l| usize::from_str_radix(&l, 2).unwrap());
  let mut len = 0usize;
  let mut counts = vec![0usize; width];
  for num in nums {
    len += 1;
    let mut num = num;
    for i in (0..width).rev() {
      counts[i] += num & 1;
      num >>= 1;
    }
  }
  let shift = 8 * size_of::<usize>() - width;
  let γ = counts.into_iter()
    .fold(0usize, |γ, count| (γ << 1) | (count > len / 2) as usize);
  let ε = !(γ << shift) >> shift;
  println!("{}", γ * ε);
}
