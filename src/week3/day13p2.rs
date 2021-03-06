use super::day13::*;

fn print_paper(paper: &Paper) {
  let width = paper.iter().max_by_key(|(x, _)| x).unwrap().0;
  let height = paper.iter().max_by_key(|(_, y)| y).unwrap().1;
  for j in 0..=height {
    for i in 0..=width {
      print!("{}", if paper.contains(&(i, j)) { '#' } else { ' ' })
    }
    println!();
  }
}

pub fn main() {
  let (mut paper, folds) = input();
  folds.into_iter().for_each(|f| fold(&mut paper, &f));
  print_paper(&paper);
}
