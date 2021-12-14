use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Polymer = Vec<char>;
pub type Rules = [[char; 26]; 26];

#[inline]
pub fn offset(c: char) -> usize {
  c as usize - 'A' as usize
}

pub fn input() -> (Polymer, Rules) {
  let file = File::open("input/day14.txt").unwrap();
  let mut lines = BufReader::new(file).lines();
  let polymer = lines.next().unwrap().unwrap().chars().collect();
  lines.next();
  let mut rules = [['\0'; 26]; 26];
  lines.for_each(|l| {
    let l = l.unwrap();
    let mut chars = l.chars();
    let c1 = chars.next().unwrap() as usize - 'A' as usize;
    let c2 = chars.next().unwrap() as usize - 'A' as usize;
    rules[c1][c2] = chars.skip(4).next().unwrap();
  });
  (polymer, rules)
}
