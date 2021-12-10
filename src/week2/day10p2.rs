use std::fs::File;
use std::io::{BufRead, BufReader};

fn score(s: String) -> u64 {
  let mut stack = Vec::with_capacity(s.len() / 4 * 3);
  for c in s.chars() {
    match c {
      '(' |'[' |  '{' | '<' => { stack.push(c); }
      ')' => { if !matches!(stack.pop(), Some('(')) { return 0; }  }
      ']' => { if !matches!(stack.pop(), Some('[')) { return 0; }  }
      '}' => { if !matches!(stack.pop(), Some('{')) { return 0; }  }
      '>' => { if !matches!(stack.pop(), Some('<')) { return 0; }  }
      _ => { panic!(); }
    }
  }
  let mut score = 0;
  while let Some(c) = stack.pop() {
    score *= 5;
    match c {
      '(' => { score += 1; }
      '[' => { score += 2; }
      '{' => { score += 3; }
      '<' => { score += 4; }
      _ => { panic!(); }
    }
  }
  score
}

pub fn main() {
  let file = File::open("input/day10.txt").unwrap();
  let mut scores = BufReader::new(file).lines()
    .map(|l| score(l.unwrap()))
    .filter(|n| *n > 0)
    .collect::<Vec<_>>();
  scores.sort_unstable();
  println!("{}", scores[scores.len() / 2]);
}
