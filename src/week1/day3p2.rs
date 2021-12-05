use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day3.txt").unwrap();
  let mut lines = BufReader::new(file).lines().map(|l| l.unwrap()).peekable();
  let width = lines.peek().unwrap().len();
  let mut nums = lines.map(|l| usize::from_str_radix(&l, 2).unwrap())
    .collect::<Vec<_>>();
  nums.sort_unstable();
  fn search<const side: bool>(nums: &Vec<usize>, width: usize) -> usize {
    let (mut left, mut right) = (0, nums.len());
    let mut criterion_bit = 1usize << width;
    let mut criterion = 0usize;
    while right - left > 1 {
      criterion_bit >>= 1;
      criterion |= criterion_bit;
      assert!(criterion >= nums[left] && criterion <= nums[right - 1]);
      let mid = nums[left..right]
        .binary_search(&criterion).unwrap_or_else(|x| x);
      if side == (mid <= (right - left) / 2) {
        left = left + mid;
      } else {
        right = left + mid;
        criterion &= !criterion_bit;
      }
    }
    nums[left]
  }
  let O2 = search::<true>(&nums, width);
  let CO2 = search::<false>(&nums, width);
  println!("{}", O2 * CO2);
}
