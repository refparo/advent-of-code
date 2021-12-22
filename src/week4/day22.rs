use std::fs::File;
use std::io::{BufRead, BufReader};

pub type Cuboid = ((i32, i32), (i32, i32), (i32, i32));
pub type Instruction = (bool, Cuboid);

pub fn input() -> impl Iterator<Item = Instruction> {
  let file = File::open("input/day22.txt").unwrap();
  BufReader::new(file).lines()
    .map(|l| {
      fn parse_eq_range(src: &str) -> (i32, i32) {
        let (_, range) = src.split_once('=').unwrap();
        let (min, max) = range.split_once("..").unwrap();
        (min.parse().unwrap(), max.parse::<i32>().unwrap() + 1)
      }
      let l = l.unwrap();
      let (op, ranges) = l.split_once(' ').unwrap();
      let (range_x, ranges_yz) = ranges.split_once(',').unwrap();
      let (range_y, range_z) = ranges_yz.split_once(',').unwrap();
      (op == "on", (
        parse_eq_range(range_x),
        parse_eq_range(range_y),
        parse_eq_range(range_z)
      ))
    })
}

fn comm(r1@(x11, _): (i32, i32), r2@(x21, _): (i32, i32))
  -> Option<(i32, i32)> {
  let ((_, x12), (x21, x22)) =
    if x11 > x21 { (r2, r1) } else { (r1, r2) };
  if x21 >= x12 { None } // [1 1) [2 2)
  else { Some((x21, x12.min(x22))) } // [1 [2 2) 1) or [1 [2 1) 2)
}

fn sub((rx, ry, rz): Cuboid, (sx, sy, sz): Cuboid) -> Vec<Cuboid> {
  let mut parts = Vec::with_capacity(6);
  fn sub1d_map_push<F>((r1, r2): (i32, i32), (s1, s2): (i32, i32),
    f: F, parts: &mut Vec<Cuboid>)
    where F: Fn((i32, i32)) -> Cuboid {
    if r1 < s1 { parts.push(f((r1, s1))); }
    if r2 > s2 { parts.push(f((s2, r2))); }
  }
  sub1d_map_push(rx, sx, |px| (px, ry, rz), &mut parts);
  sub1d_map_push(ry, sy, |py| (sx, py, rz), &mut parts);
  sub1d_map_push(rz, sz, |pz| (sx, sy, pz), &mut parts);
  parts
}

fn step(reactor: &mut Vec<Cuboid>, (op, area@(ax, ay, az)): Instruction) {
  let mut i = 0;
  while i < reactor.len() {
    let refn@(rx, ry, rz) = reactor[i];
    if let (Some(cx), Some(cy), Some(cz))
      = (comm(rx, ax), comm(ry, ay), comm(rz, az)) {
      let comm = (cx, cy, cz);
      sub(refn, comm).into_iter()
        .for_each(|part| { reactor.push(part); });
      reactor.swap_remove(i);
    } else {
      i += 1;
    }
  }
  if op {
    reactor.push(area);
  }
}

pub fn reboot<T: Iterator<Item = Instruction>>(instr: T) -> Vec<Cuboid> {
  let mut reactor = Vec::with_capacity(1024);
  instr.for_each(|instr| step(&mut reactor, instr));
  reactor
}

pub fn count(reactor: &Vec<Cuboid>) -> usize {
  let mut count = 0;
  reactor.iter().for_each(|&((x1, x2), (y1, y2), (z1, z2))| {
    count += (x2 - x1) as usize * (y2 - y1) as usize * (z2 - z1) as usize;
  });
  count
}
