use std::collections::{HashSet, VecDeque};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::ops::{Add, Sub, Mul};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub enum Vector<T, const n: usize> { MkVector([T; n]) }
pub use Vector::*;

impl<T, const n: usize> Add for Vector<T, n>
  where T: Copy + Add<Output = T> {
  type Output = Vector<T, n>;
  fn add(self, MkVector(rhs): Vector<T, n>) -> Vector<T, n> {
    let MkVector(mut lhs) = self;
    lhs.iter_mut().zip(rhs).for_each(|(a, b)| *a = *a + b);
    MkVector(lhs)
  }
}

impl<T, const n: usize> Sub for Vector<T, n>
  where T: Copy + Sub<Output = T> {
  type Output = Vector<T, n>;
  fn sub(self, MkVector(rhs): Vector<T, n>) -> Vector<T, n> {
    let MkVector(mut lhs) = self;
    lhs.iter_mut().zip(rhs).for_each(|(a, b)| *a = *a - b);
    MkVector(lhs)
  }
}

impl<T, const n: usize> Mul<T> for Vector<T, n>
  where T: Copy + Mul<Output = T> {
  type Output = Vector<T, n>;
  fn mul(self, k: T) -> Vector<T, n> {
    let MkVector(mut lhs) = self;
    lhs.iter_mut().for_each(|a| *a = *a * k);
    MkVector(lhs)
  }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Matrix<T, const m: usize, const n: usize>
  { MkMatrix([Vector<T, m>; n]) }
pub use Matrix::*;

impl<T, const m: usize, const n: usize> Mul<Vector<T, n>> for &Matrix<T, m, n>
  where T: Copy + Add<Output = T> + Mul<Output = T> {
  type Output = Vector<T, m>;
  fn mul(self, MkVector(rhs): Vector<T, n>) -> Vector<T, m> {
    let MkMatrix(lhs) = self;
    lhs.into_iter().zip(rhs)
      .map(|(v, k)| *v * k)
      .reduce(|a, b| a + b).unwrap()
  }
}

impl<T, const m: usize, const n: usize, const p: usize>
  Mul<Matrix<T, n, p>> for &Matrix<T, m, n>
  where T: Copy + Add<Output = T> + Mul<Output = T> {
  type Output = Matrix<T, m, p>;
  fn mul(self, MkMatrix(rhs): Matrix<T, n, p>) -> Matrix<T, m, p> {
    let MkMatrix(lhs) = self;
    let mut res = [lhs[0]; p];
    res.iter_mut().zip(rhs).for_each(|(r, v)| *r = self * v);
    MkMatrix(res)
  }
}

pub type Vec3 = Vector<i16, 3>;
pub type Mat3 = Matrix<i16, 3, 3>;

pub fn rotation3() -> [Mat3; 24] {
  let id = MkMatrix([
    MkVector([1, 0, 0]),
    MkVector([0, 1, 0]),
    MkVector([0, 0, 1])
  ]);
  let xz = MkMatrix([
    MkVector([ 0, 0, 1]),
    MkVector([ 0, 1, 0]),
    MkVector([-1, 0, 0])
  ]);
  let xy = MkMatrix([
    MkVector([ 0, 1, 0]),
    MkVector([-1, 0, 0]),
    MkVector([ 0, 0, 1])
  ]);
  let yz = MkMatrix([
    MkVector([1,  0, 0]),
    MkVector([0,  0, 1]),
    MkVector([0, -1, 0])
  ]);
  let mut res = [id; 24];
  [id, xz, &xz * xz, &xz * (&xz * xz)]
    .into_iter().flat_map(|rot| [
      rot, &xy * rot, &xy * (&xy * rot), &xy * (&xy * (&xy * rot)),
           &yz * rot,                    &yz * (&yz * (&yz * rot))
    ]).zip(res.iter_mut()).for_each(|(rot, res)| *res = rot);
  res
}

pub fn input() -> Vec<Vec<Vec3>> {
  let mut res = Vec::with_capacity(30);
  let file = File::open("input/day19.txt").unwrap();
  let mut lines = BufReader::new(file).lines();
  while let Some(Ok(_)) = lines.next() {
    let mut scanner = Vec::with_capacity(30);
    while let Some(Ok(line)) = lines.next() {
      if line.len() == 0 { break; }
      let (x, yz) = line.split_once(',').unwrap();
      let (y, z) = yz.split_once(',').unwrap();
      scanner.push(MkVector([
        x.parse().unwrap(), y.parse().unwrap(), z.parse().unwrap()]));
    }
    res.push(scanner);
  }
  res
}

pub fn compare<'a>(this: &Vec<Vec3>, other: &Vec<Vec3>,
  rotations: &'a [Mat3; 24]) -> Option<(&'a Mat3, Vec3, Vec3)> {
  // b1s[n] = This - this[n]
  let b1s = this.iter()
    .map(|orig| this.iter().map(|b| *b - *orig).collect::<HashSet<_>>())
    .collect::<Vec<_>>();
  // b2s[24n+r] = rot[r] * (Other - other[n])
  let b2s = other.iter()
    .flat_map(|orig| rotations.iter()
      .map(|rot| other.iter()
        .map(|b| rot * (*b - *orig)).collect::<HashSet<_>>()))
    .collect::<Vec<_>>();
  let mut i = 0;
  while i < this.len() && i < other.len() {
    let b1 = &b1s[i];
    for (j, b2) in b2s[i * 24..].iter().enumerate() {
      if b1.intersection(b2).count() >= 12 {
        let r = j % 24;
        let (i, j) = (i, i + j / 24);
        return Some((&rotations[r], this[i], other[j]))
      }
    }
    i += 1;
    if i >= other.len() { break; }
    for (r, b2) in b2s[i * 24..i * 24 + 24].iter().enumerate() {
      for (j, b1) in b1s[i..].iter().enumerate() {
        if b2.intersection(b1).count() >= 12 {
          let (i, j) = (j + i, i);
          return Some((&rotations[r], this[i], other[j]))
        }
      }
    }
    i += 1;
  }
  None
}

pub struct State {
  pub rotations: [Mat3; 24],
  pub inputs: Vec<Vec<Vec3>>,
  pub beacons: HashSet<Vec3>,
  pub unmatched: HashSet<usize>,
  pub references: VecDeque<usize>,
  pub scanners: Vec<Vec3>,
}
impl State {
  pub fn new() -> State {
    let rotations = rotation3();
    let inputs = input();
    let mut beacons = HashSet::with_capacity(15 * inputs[0].len());
    inputs[0].iter().for_each(|b| { beacons.insert(*b); });
    let unmatched = (0..inputs.len()).collect::<HashSet<_>>();
    let references = VecDeque::from([0]);
    let scanners = Vec::with_capacity(inputs.len());
    State { rotations, inputs, beacons, unmatched, references, scanners }
  }
  pub fn solve(&mut self) {
    while let Some(ref_idx) = self.references.pop_front() {
      self.unmatched.iter()
        .filter_map(|&i| Some((i, compare(
          &self.inputs[ref_idx], &self.inputs[i], &self.rotations)?)))
        .collect::<Vec<_>>().into_iter()
        .for_each(|(i, (mat, this, other))| {
          self.unmatched.remove(&i);
          self.inputs[i].iter_mut().for_each(|b| {
            *b = mat * (*b - other) + this;
            self.beacons.insert(*b);
          });
          self.references.push_back(i);
          let scanner = mat * (MkVector([0, 0, 0]) - other) + this;
          self.scanners.push(scanner);
          println!("match! {} <- scanner {} at {:?}", ref_idx, i, scanner);
        })
    }
  }
}
