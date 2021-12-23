use std::fmt;
use std::fmt::{Display, Formatter};

pub const input: [(u32, u32); 4] =
  if false { [
    (10, 1),
    (100, 1000),
    (10, 100),
    (1000, 1)
  ] } else { [
    (1000, 100),
    (1, 1),
    (100, 10),
    (1000, 10)
  ] };

#[derive(Clone, Copy, Debug)]
pub struct Burrow<const n: usize> {
  pub cost: u32,
  pub side_rooms: [[u32; n]; 4],
  pub hallway: [u32; 7]
}

pub trait NewBurrow: Sized {
  fn new(side_rooms_in: [(u32, u32); 4]) -> Self;
}

impl<const n: usize> Burrow<n> {
  pub fn try_move<const direction: bool>(&self, from: usize) -> Option<Self> {
    if direction && from < 6 {
      if self.hallway[from + 1] == 0 {
        let mut next = *self;
        next.cost += next.hallway[from]
          * if matches!(from, 0 | 5) { 1 } else { 2 };
        next.hallway.swap(from, from + 1);
        Some(next)
      } else { None }
    } else if !direction && from > 0 {
      if self.hallway[from - 1] == 0 {
        let mut next = *self;
        next.cost += next.hallway[from]
          * if matches!(from, 1 | 6) { 1 } else { 2 };
        next.hallway.swap(from, from - 1);
        Some(next)
      } else { None }
    } else { None }
  }

  fn come_out(&self, from: usize) -> Vec<Self> {
    let mut cases = Vec::with_capacity(7);
    let mut out = *self;
    if {
      let host = 10u32.pow(from as u32);
      self.side_rooms[from].iter().all(|&x| x == 0 || x == host)
    } { return cases; }
    let (amphi, dist) = if let Some(res) =
      out.side_rooms[from].iter_mut().enumerate()
        .find_map(|(i, x)| if *x > 0 {
          let res = (*x, i as u32 + 2);
          *x = 0;
          Some(res)
        } else { None })
      { res } else { return cases; };
    out.cost += amphi * dist;
    let out = out;
    if out.hallway[from + 1] == 0 {
      let mut left = out;
      left.hallway[from + 1] = amphi;
      cases.push(left);
      let mut from = from + 1;
      while let Some(step) = left.try_move::<false>(from) {
        left = step;
        cases.push(left);
        from -= 1;
      }
    }
    if out.hallway[from + 2] == 0 {
      let mut right = out;
      right.hallway[from + 2] = amphi;
      cases.push(right);
      let mut from = from + 2;
      while let Some(step) = right.try_move::<true>(from) {
        right = step;
        cases.push(right);
        from += 1;
      }
    }
    cases
  }

  fn any_come_out(&self) -> impl Iterator<Item = Self> {
    self.come_out(0).into_iter()
      .chain(self.come_out(1))
      .chain(self.come_out(2))
      .chain(self.come_out(3))
  }

  fn try_in(&self, mut from: usize) -> Option<Self> {
    let room = match self.hallway[from] {
      0 => { return None; }
      1 => { 0 }
      10 => { 1 }
      100 => { 2 }
      1000 => { 3 }
      _ => { panic!(); }
    };
    let part = if let Some(res) =
      self.side_rooms[room].iter().enumerate().rev()
        .find_map(|(i, x)| if *x == 0 { Some(i) } else { None })
      { res } else { return None; };
    if part < n - 1 && (self.side_rooms[room][part + 1] != self.hallway[from]
      || self.side_rooms[room][n - 1] != self.hallway[from]) {
      return None;
    }
    let mut moving = *self;
    while from < room + 1 {
      if let Some(step) = moving.try_move::<true>(from) {
        moving = step;
        from += 1;
      } else { break }
    }
    while from > room + 2 {
      if let Some(step) = moving.try_move::<false>(from) {
        moving = step;
        from -= 1;
      } else { break }
    }
    if from == room + 1 || from == room + 2 {
      moving.side_rooms[room][part] = moving.hallway[from];
      moving.cost += moving.hallway[from] * (2 + part as u32);
      moving.hallway[from] = 0;
      Some(moving)
    } else { None }
  }

  fn any_try_in(&self) -> Vec<Self> {
    let mut cases = Vec::with_capacity(7);
    for i in 0..7 {
      if let Some(res) = self.try_in(i) {
        cases.push(res);
      }
    }
    cases
  }

  fn done(&self) -> bool {
    self.side_rooms[0].iter().all(|x| *x == 1)
      && self.side_rooms[1].iter().all(|x| *x == 10)
      && self.side_rooms[2].iter().all(|x| *x == 100)
      && self.side_rooms[3].iter().all(|x| *x == 1000)
  }

  pub fn solve(&self) -> Self {
    let mut min = None::<Self>;
    let mut cases = Vec::<Self>::from([*self]);
    while let Some(case) = cases.pop() {
      let case = case;
      case.any_come_out()
        .for_each(|case| 
          if case.cost < min.map_or(u32::MAX, |c| c.cost) {
            if case.done() {
              min = Some(case);
            } else {
              cases.push(case);
            }
          });
      case.any_try_in().into_iter()
        .for_each(|case|
          if case.cost < min.map_or(u32::MAX, |c| c.cost) {
            if case.done() {
              min = Some(case);
            } else {
              cases.push(case);
            }
          });
    }
    min.unwrap()
  }
}

impl<const n: usize> Display for Burrow<n> {
  fn fmt(&self, f: &mut Formatter) -> Result<(), fmt::Error> {
    fn amphi(x: u32) -> Result<char, fmt::Error> {
      match x {
        0 => { Ok('.') }
        1 => { Ok('A') }
        10 => { Ok('B') }
        100 => { Ok('C') }
        1000 => { Ok('D') }
        _ => { Err(fmt::Error) }
      }
    }
    write!(f, "cost={}\n", self.cost)?;
    write!(f, "#############\n")?;
    write!(f, "#{}{}.{}.{}.{}.{}{}#\n",
      amphi(self.hallway[0])?,
      amphi(self.hallway[1])?,
      amphi(self.hallway[2])?,
      amphi(self.hallway[3])?,
      amphi(self.hallway[4])?,
      amphi(self.hallway[5])?,
      amphi(self.hallway[6])?)?;
    write!(f, "###{}#{}#{}#{}###\n",
      amphi(self.side_rooms[0][0])?,
      amphi(self.side_rooms[1][0])?,
      amphi(self.side_rooms[2][0])?,
      amphi(self.side_rooms[3][0])?)?;
    for i in 1..n {
      write!(f, "  #{}#{}#{}#{}#\n",
        amphi(self.side_rooms[0][i])?,
        amphi(self.side_rooms[1][i])?,
        amphi(self.side_rooms[2][i])?,
        amphi(self.side_rooms[3][i])?)?;
    }
    write!(f, "  #########\n")?;
    Ok(())
  }
}
