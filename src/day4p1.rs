use super::day4::*;

pub fn main() {
  let (numbers, mut boards) = input();
  for num in numbers {
    for board in boards.iter_mut() {
      if let Some(score) = mark(board, num) {
        println!("{}", score);
        return;
      }
    }
  }
}
