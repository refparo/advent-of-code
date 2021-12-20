use super::day20::*;

pub fn main() {
  let (alg, mut img) = input();
  for _ in 0..50 { img = step(img, &alg); }
  println!("{}", img.1.into_iter().filter(|p| *p).count());
}
