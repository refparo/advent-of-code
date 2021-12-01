use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn main() {
  let file = File::open("input/day1.txt").unwrap();
  let mut iter = BufReader::new(file)
    .lines()
    .map(|x| x.unwrap().parse::<u32>().unwrap());
  let mut inc = 0;
  let mut fst = iter.next().unwrap();
  let mut snd = iter.next().unwrap();
  let mut thrd = iter.next().unwrap();
  iter.fold(fst + snd + thrd, |prev, frth| {
    let next = prev - fst + frth;
    if prev < next { inc += 1; }
    fst = snd; snd = thrd; thrd = frth;
    next
  });
  println!("{}", inc);
}
