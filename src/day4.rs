use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn input() -> (Vec<u8>, Vec<Vec<Vec<u8>>>) {
  let file = File::open("input/day4.txt").unwrap();
  let mut lines = BufReader::new(file).lines();
  let numbers = lines.next().unwrap().unwrap()
    .split(',').map(|s| s.parse().unwrap())
    .collect();
  let mut boards = Vec::with_capacity(100);
  while let Some(_) = lines.next() {
    boards.push((0..5)
      .map(|_| lines.next().unwrap().unwrap()
        .split_ascii_whitespace()
        .map(|s| s.parse().unwrap())
        .collect())
      .collect())
  }
  (numbers, boards)
}

pub fn mark(board: &mut Vec<Vec<u8>>, target: u8) -> Option<u32> {
  let mut pos = Option::<(usize, usize)>::None;
  'outer: for (i, line) in board.iter_mut().enumerate() {
    for (j, num) in line.iter_mut().enumerate() {
      if *num == target {
        *num = !target;
        pos = Some((i, j));
        break 'outer;
      }
    }
  }
  if let Some((i, j)) = pos {
    if (&board[i]).into_iter().all(|num| num >> 7 > 0)
      || board.into_iter().all(|l| l[j] >> 7 > 0) { Some(
      board.into_iter()
        .map(|l| l.into_iter()
          .filter(|num| **num >> 7 == 0)
          .map(|num| *num as u32).sum::<u32>())
        .sum::<u32>() * target as u32
    ) } else { None }
  } else { None }
}
