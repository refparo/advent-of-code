use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Paper = HashSet<(u32, u32)>;
pub type Folds = Vec<(bool, u32)>;

pub fn input() -> (Paper, Folds) {
  let file = File::open("input/day13.txt").unwrap();
  let mut lines = BufReader::new(file).lines();
  let mut points = HashSet::with_capacity(1024);
  while let Some(Ok(line)) = lines.next() {
    if line.len() == 0 { break; }
    let (a, b) = line.split_once(',').unwrap();
    points.insert((a.parse().unwrap(), b.parse().unwrap()));
  }
  let folds = lines.map(|l| {
    let l = l.unwrap();
    let (direction, axis) = l.split_once('=').unwrap();
    (direction.chars().rev().next().unwrap() == 'x', axis.parse().unwrap())
  }).collect();
  (points, folds)
}

pub fn fold(paper: &mut Paper, (direction, axis): &(bool, u32)) {
  if *direction {
    let points = paper.iter()
      .filter(|(x, _)| x > axis)
      .map(|p| *p)
      .collect::<Vec<_>>();
    points.into_iter().for_each(|p@(x, y)| {
      paper.remove(&p);
      paper.insert((2 * axis - x, y));
    })
  } else {
    let points = paper.iter()
      .filter(|(_, y)| y > axis)
      .map(|p| *p)
      .collect::<Vec<_>>();
    points.into_iter().for_each(|p@(x, y)| {
      paper.remove(&p);
      paper.insert((x, 2 * axis - y));
    })
  }
}
