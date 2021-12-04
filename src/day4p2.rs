use super::day4::{input, mark};

pub fn main() {
  let (numbers, mut boards) = input();
  let mut wins = vec![false; boards.len()];
  let mut last_score = 0;
  for num in numbers {
    for (i, win) in wins.iter_mut().enumerate().filter(|(_, i)| !**i) {
      if let Some(score) = mark(&mut boards[i], num) {
        *win = true;
        last_score = score;
      }
    }
    if (&wins).into_iter().all(|x| *x) { break; }
  }
  println!("{}", last_score);
}
