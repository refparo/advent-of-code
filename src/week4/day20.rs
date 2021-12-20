use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Algorithm = Vec<bool>;
pub type Image = (usize, Vec<bool>);

pub fn input() -> (Algorithm, Image) {
  let file = File::open("input/day20.txt").unwrap();
  let mut lines = BufReader::new(file).lines();
  let alg = lines.next().unwrap().unwrap()
    .chars().map(|c| c == '#').collect();
  lines.next();
  let mut lines = lines.peekable();
  let size = lines.peek().unwrap().as_ref().unwrap().len() + 4;
  let mut img = Vec::with_capacity(size * size);
  for _ in 0..size { img.push(false); }
  for _ in 0..size { img.push(false); }
  lines.for_each(|l| {
    img.push(false); img.push(false);
    l.unwrap().chars().for_each(|c| img.push(c == '#'));
    img.push(false); img.push(false);
  });
  for _ in 0..size { img.push(false); }
  for _ in 0..size { img.push(false); }
  (alg, (size, img))
}

pub fn step((size, img): Image, alg: &Algorithm) -> Image {
  let size1 = size + 2;
  let mut img1 = Vec::with_capacity(size1 * size1);
  let fill = match img[0] { false => { alg[0] } true => { alg[(1 << 9) - 1] } };
  for _ in 0..size1 { img1.push(fill); }
  for _ in 0..size1 { img1.push(fill); }
  for i in 2..size1 - 2 {
    img1.push(fill); img1.push(fill);
    for j in 2..size1 - 2 {
      let mut addr = 0;
      addr |= img[(i - 2) * size + (j - 2)] as usize;
      addr <<= 1;
      addr |= img[(i - 2) * size + (j - 1)] as usize;
      addr <<= 1;
      addr |= img[(i - 2) * size + j] as usize;
      addr <<= 1;
      addr |= img[(i - 1) * size + (j - 2)] as usize;
      addr <<= 1;
      addr |= img[(i - 1) * size + (j - 1)] as usize;
      addr <<= 1;
      addr |= img[(i - 1) * size + j] as usize;
      addr <<= 1;
      addr |= img[i * size + (j - 2)] as usize;
      addr <<= 1;
      addr |= img[i * size + (j - 1)] as usize;
      addr <<= 1;
      addr |= img[i * size + j] as usize;
      img1.push(alg[addr]);
    }
    img1.push(fill); img1.push(fill);
  }
  for _ in 0..size1 { img1.push(fill); }
  for _ in 0..size1 { img1.push(fill); }
  (size1, img1)
}
