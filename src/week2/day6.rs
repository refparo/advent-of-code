use std::collections::VecDeque;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[inline]
pub fn fish<const days: usize>() {
  let file = File::open("input/day6.txt").unwrap();
  let mut ring = VecDeque::from([0; 9]);
  for num in BufReader::new(file).lines()
    .next().unwrap().unwrap().split(',') {
    ring[num.parse::<usize>().unwrap()] += 1;
  }
  for _ in 0..days {
    let birth = ring.pop_front().unwrap();
    ring[6] += birth;
    ring.push_back(birth);
  }
  println!("{}", ring.into_iter().sum::<u64>());
}
