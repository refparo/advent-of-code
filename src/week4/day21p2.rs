use std::collections::HashMap;
use std::hash::Hash;
use std::ops::AddAssign;

use super::day21::*;

#[derive(Eq, Hash, PartialEq)]
enum Universe { Gaming(u32, u32, u32, u32), P1Win, P2Win }
use Universe::*;
type State = HashMap<Universe, usize>;

#[inline]
fn insert_add<K, V>(state: &mut HashMap<K, V>, k: K, v: V)
  where K: Eq + Hash, V: AddAssign {
  if let Some(v0) = state.get_mut(&k) {
    *v0 += v;
  } else {
    state.insert(k, v);
  }
}

/// should have been named `3d3` but identifiers can't start with numbers
const dice3: [(u32, usize); 7] =
  [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)];

fn step(state: State) -> State {
  let mut state1 = State::with_capacity(state.len() * 3);
  state.into_iter().for_each(|(u, n)| {
    match u {
      Gaming(p1, s1, p2, s2) => {
        for (d1, k) in dice3.into_iter() {
          let p11 = (p1 + d1 - 1) % 10 + 1;
          let s11 = s1 + p11;
          if s11 >= 21 {
            insert_add(&mut state1, P1Win, n * k);
            continue;
          }
          for (d2, m) in dice3.into_iter() {
            let p21 = (p2 + d2 - 1) % 10 + 1;
            let s21 = s2 + p21;
            if s21 >= 21 {
              insert_add(&mut state1, P2Win, n * k * m);
            } else {
              insert_add(&mut state1, Gaming(p11, s11, p21, s21), n * k * m);
            }
          }
        }
      }
      _ => { insert_add(&mut state1, u, n); }
    }
  });
  state1
}

pub fn main() {
  let (p1, p2) = input;
  let mut state = State::from([(Gaming(p1, 0, p2, 0), 1)]);
  state = step(state);
  while state.len() > 2 { state = step(state); }
  println!("{}", state[&P1Win].max(state[&P2Win]));
}
