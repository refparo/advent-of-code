use super::day13::*;

pub fn main() {
  let (mut paper, folds) = input();
  fold(&mut paper, &folds[0]);
  println!("{}", paper.len());
}
