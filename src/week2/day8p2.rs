use std::fs::File;
use std::io::{BufRead, BufReader};

trait FindRemove {
  type Item;
  fn find_remove<P>(&mut self, predicate: P) -> Option<Self::Item>
    where Self: Sized, P: Fn(&Self::Item) -> bool;
}
impl<T> FindRemove for Vec<T> {
  type Item = T;
  fn find_remove<P>(&mut self, p: P) -> Option<Self::Item>
    where Self: Sized, P: FnMut(&Self::Item) -> bool {
    Some(self.swap_remove(self.iter().position(p).unwrap()))
  }
}

pub fn main() {
  let file = File::open("input/day8.txt").unwrap();
  println!("{}", BufReader::new(file).lines()
    .map(|line| {
      let line = line.unwrap();
      let mut display = line.split_ascii_whitespace().map(|s| {
        let mut chars = s.chars().collect::<Vec<_>>();
        chars.sort_unstable();
        chars.into_iter().collect::<String>()
      }).collect::<Vec<_>>();
      let input = display.split_off(10);
      let mut mapping: [String; 10] = Default::default();
      mapping[1] = display.find_remove(|s| s.len() == 2).unwrap();
      mapping[4] = display.find_remove(|s| s.len() == 4).unwrap();
      mapping[7] = display.find_remove(|s| s.len() == 3).unwrap();
      mapping[8] = display.find_remove(|s| s.len() == 7).unwrap();
      let bd = mapping[4].chars()
        .filter(|c| mapping[1].find(*c).is_none())
        .collect::<String>();
      mapping[3] = display.find_remove(|s| s.len() == 5 &&
        mapping[1].chars().all(|c| s.find(c).is_some())).unwrap();
      mapping[5] = display.find_remove(|s| s.len() == 5 &&
        bd.chars().all(|c| s.find(c).is_some())).unwrap();
      mapping[2] = display.find_remove(|s| s.len() == 5).unwrap();
      mapping[0] = display.find_remove(|s| s.len() == 6 &&
        !bd.chars().all(|c| s.find(c).is_some())).unwrap();
      mapping[9] = display.find_remove(|s| s.len() == 6 &&
        mapping[1].chars().all(|c| s.find(c).is_some())).unwrap();
      mapping[6] = display.swap_remove(0);
      input.into_iter().skip(1)
        .map(|s| mapping.iter().enumerate()
          .find(|(_, t)| **t == s).unwrap().0)
        .reduce(|res, d| res * 10 + d).unwrap()
    })
    .sum::<usize>());
}
