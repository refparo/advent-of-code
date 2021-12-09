use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn input() -> Vec<Vec<u32>> {
  let file = File::open("input/day9.txt").unwrap();
  BufReader::new(file).lines()
    .map(|l| l.unwrap().chars()
      .map(|c| c.to_digit(10).unwrap())
      .collect::<Vec<_>>())
    .collect::<Vec<_>>()
}

pub fn low_points<'a>(map: &'a Vec<Vec<u32>>)
  -> impl 'a + Iterator<Item = (usize, usize)> {
  map.iter().enumerate()
    .flat_map(move |(i, row)| {
      row.iter().enumerate()
        .filter(move |(j, h)| (*j == 0 || row[*j - 1] > **h) &&
          (*j == row.len() - 1 || row[*j + 1] > **h) &&
          (i == 0 || map[i - 1][*j] > **h) &&
          (i == map.len() - 1 || map[i + 1][*j] > **h))
        .map(move |(j, _)| (i, j))
    })
}
