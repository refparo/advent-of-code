use super::day19::*;

pub fn main() {
  let mut state = State::new();
  state.solve();
  assert!(state.unmatched.is_empty());
  let dist = state.scanners.iter().enumerate()
    .flat_map(|(i, s1)| state.scanners[i + 1..].iter().map(|s2| {
      let MkVector([x, y, z]) = *s1 - *s2;
      x.abs() + y.abs() + z.abs()
    })).max().unwrap();
  println!("{}", dist);
}
