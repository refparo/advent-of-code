use std::fs::File;
use std::io::{BufRead, BufReader};

fn score(s: String) -> u32 {
  let mut stack = Vec::with_capacity(s.len() / 4 * 3);
  for c in s.chars() {
    match c {
      '(' |'[' |  '{' | '<' => { stack.push(c); }
      ')' => { if !matches!(stack.pop(), Some('(')) { return 3; }  }
      ']' => { if !matches!(stack.pop(), Some('[')) { return 57; }  }
      '}' => { if !matches!(stack.pop(), Some('{')) { return 1197; }  }
      '>' => { if !matches!(stack.pop(), Some('<')) { return 25137; }  }
      _ => { panic!(); }
    }
  }
  0
}

pub fn main() {
  let file = File::open("input/day10.txt").unwrap();
  println!("{}", BufReader::new(file).lines()
    .map(|l| score(l.unwrap())).sum::<u32>());
}
