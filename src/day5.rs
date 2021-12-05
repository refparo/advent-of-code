use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Point = (u16, u16);
pub type Line = (Point, Point);
pub type Map = [[u8; 1000]; 1000];

#[inline]
fn sort<T: PartialOrd>(a: T, b: T) -> (T, T) {
  if a < b { (a, b) } else { (b, a) }
}

#[inline]
fn parse_point(s: &str) -> Point {
  let (x, y) = s.split_once(",").unwrap();
  (x.parse().unwrap(), y.parse().unwrap())
}

pub fn input() -> Vec<Line> {
  let file = File::open("input/day5.txt").unwrap();
  BufReader::new(file).lines()
    .map(|l| match l.unwrap().split_once(" -> ").unwrap() {
      (p1, p2) => (parse_point(p1), parse_point(p2))
    })
    .collect::<Vec<_>>()
}

#[inline]
pub fn draw(((x1, y1), (x2, y2)): Line, map: &mut Map) {
  if y1 == y2 {
    let (x1, x2) = sort(x1 as usize, x2 as usize);
    for j in x1..x2 + 1 { map[y1 as usize][j] += 1; }
  } else if x1 == x2 {
    let (y1, y2) = sort(y1 as usize, y2 as usize);
    for i in y1..y2 + 1 { map[i][x1 as usize] += 1; }
  } else if (x1 < x2) == (y1 < y2) {
    let ((x, y), (xend, _)) =
      sort((x1 as usize, y1 as usize), (x2 as usize, y2 as usize));
    for i in 0..xend - x + 1 { map[y + i][x + i] += 1; }
  } else {
    let ((y, x), (yend, _)) =
      sort((y1 as usize, x1 as usize), (y2 as usize, x2 as usize));
    for i in 0..yend - y + 1 { map[y + i][x - i] += 1; }
  }
}

pub fn count(map: &Map) -> usize {
  let mut count = 0usize;
  for row in map {
    for &point in row {
      if point >= 2 { count += 1; }
    }
  }
  count
}
