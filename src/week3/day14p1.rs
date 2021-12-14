/// A naive solution, but complex enough to be preserved.

use std::mem::swap;

use super::day14::*;

fn insert(template: &Polymer, rules: &Rules, output: &mut Polymer) {
  output.clear();
  for pair in template.windows(2) {
    output.push(pair[0]);
    let insertion = rules[offset(pair[0])][offset(pair[1])];
    if insertion != '\0' {
      output.push(insertion);
    }
  }
  output.push(template[template.len() - 1]);
}

fn count_most_common<T: PartialEq, const least: bool>(xs: &[T]) -> usize {
  let mut count = if least { usize::max_value() } else { 0 };
  let mut temp = 1;
  for pair in xs.windows(2) {
    if pair[0] == pair[1] {
      temp += 1;
    } else {
      if (temp > count) != least {
        count = temp;
      }
      temp = 1;
    }
  }
  if (temp > count) != least {
    count = temp;
  }
  count
}

pub fn main() {
  let (mut output, rules) = input();
  output.reserve(1024 - output.len());
  let mut template = Vec::with_capacity(1024);
  for _ in 0..10 {
    swap(&mut template, &mut output);
    insert(&template, &rules, &mut output);
  }
  output.sort_unstable();
  println!("{}", count_most_common::<_, false>(&output)
    - count_most_common::<_, true>(&output));
}
