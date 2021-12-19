use super::day19::*;

pub fn main() {
  let mut state = State::new();
  state.solve();
  assert!(state.unmatched.is_empty());
  println!("{}", state.beacons.len());
}
