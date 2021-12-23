use super::day21::*;

// 1+2+3 -> 6
// 4+5+6 -> 15 -> 5
// (5+9)%10 -> 4
// (4+9)%10 -> 3
// 2, 1, 0, 9, 8, 7...
// (97+98+99)%10 -> 4
// (100+1+2)%10 -> 3
// => dice(n) = (16 - n % 10) % 10

pub fn main() {
  let (mut p1, mut p2) = input;
  let (mut s1, mut s2) = (0, 0);
  let mut dice = 0;
  loop {
    p1 = (p1 + 15 - dice % 10) % 10 + 1;
    dice += 1;
    s1 += p1;
    if s1 >= 1000 {
      println!("P1 wins! {}", s2 * dice * 3);
      break;
    }
    p2 = (p2 + 15 - dice % 10) % 10 + 1;
    dice += 1;
    s2 += p2;
    if s2 >= 1000 {
      println!("P2 wins! {}", s1 * dice * 3);
      break;
    }
  }
}
