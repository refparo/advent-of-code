// This solution is also appliable to part 1.

use super::day14::*;

type Pairs = [[usize; 26]; 26];
type Elements = [usize; 26];
type Extract = (Pairs, Elements);

fn extract(template: Polymer) -> Extract {
  let mut pairs = [[0; 26]; 26];
  let mut elements = [0; 26];
  elements[offset(template[0])] += 1;
  for pair in (&template).windows(2) {
    pairs[offset(pair[0])][offset(pair[1])] += 1;
    elements[offset(pair[1])] += 1;
  }
  (pairs, elements)
}

fn insert((pair, elements): Extract, rules: &Rules) -> Extract {
  let mut new_pair = [[0; 26]; 26];
  let mut new_elements = elements;
  for (i, row) in rules.iter().enumerate() {
    for (j, c) in row.iter().enumerate() {
      if *c != '\0' && pair[i][j] > 0 {
        let c = offset(*c);
        new_elements[c] += pair[i][j];
        new_pair[i][c] += pair[i][j];
        new_pair[c][j] += pair[i][j];
      }
    }
  }
  (new_pair, new_elements)
}

pub fn main() {
  let (template, rules) = input();
  let mut extract = extract(template);
  for _ in 0..40 {
    extract = insert(extract, &rules);
  }
  println!("{}", extract.1.iter().max().unwrap()
    - extract.1.iter().filter(|n| **n > 0).min().unwrap());
}
