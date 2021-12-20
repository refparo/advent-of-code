use super::day20::*;

pub fn main() {
  let (alg, img) = input();
  let img = step(step(img, &alg), &alg);
  println!("{}", img.1.into_iter().filter(|p| *p).count());
}
