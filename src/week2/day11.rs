use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Map = [[u8; 10]; 10];

pub fn input() -> Map {
  let file = File::open("input/day11.txt").unwrap();
  let mut map = [[0u8; 10]; 10];
  for (i, l) in BufReader::new(file).lines().enumerate() {
    for (j, c) in l.unwrap().chars().enumerate() {
      map[i][j] = c.to_digit(10).unwrap() as u8;
    }
  }
  map
}

pub fn step(map: &mut Map) -> usize {
  for l in map.iter_mut() {
    for octo in l.iter_mut() {
      *octo += 1;
    }
  }
  let mut flashed = Vec::with_capacity(32);
  let mut count = 0;
  loop {
    for i in 0..map.len() {
      for j in 0..map[i].len() {
        if map[i][j] > 9 {
          flashed.push((i, j));
          for i in i.max(1) - 1..(i + 2).min(10) {
            for j in j.max(1) - 1..(j + 2).min(10) {
              if map[i][j] > 0 { map[i][j] += 1; }
            }
          }
        }
      }
    }
    if flashed.is_empty() { break; }
    count += flashed.len();
    while let Some((i, j)) = flashed.pop() {
      map[i][j] = 0;
    }
  }
  count
}
