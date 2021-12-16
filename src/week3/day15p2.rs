// Unfortunately, it does in part 2. So we have to use Djikstra's algorithm.
// Implemented using HashSet, because using BinaryHeap is too troublesome.
// It's REEEEALLY SLOOOOWW
// But I DON'T FUCKING CARE

use std::collections::HashSet;

use super::day15::*;

fn neighbors(width: usize)
  -> impl Fn(usize, usize, usize, usize) -> Vec<(usize, usize, usize, usize)> {
  move |i, j, k, m| {
    let mut vec = Vec::with_capacity(4);
    if i > 0 {
      vec.push((i - 1, j, k, m));
    } else if k > 0 {
      vec.push((width - 1, j, k - 1, m));
    }
    if j > 0 {
      vec.push((i, j - 1, k, m));
    } else if m > 0 {
      vec.push((i, width - 1, k, m - 1));
    }
    if i < width - 1 {
      vec.push((i + 1, j, k, m));
    } else if k < 4 {
      vec.push((0, j, k + 1, m));
    }
    if j < width - 1 {
      vec.push((i, j + 1, k, m));
    } else if m < 4 {
      vec.push((i, 0, k, m + 1));
    }
    vec
  }
}

#[inline]
fn risk(orig: u32, k: usize, m: usize) -> u32 {
  (orig + k as u32 + m as u32 - 1) % 9 + 1
}

fn dijkstra(map: &Map, width: usize) -> u32 {
  let neighbors = neighbors(width);
  let mut dist_map = vec![[[(false, u32::MAX); 5]; 5]; map.len()];
  dist_map[0][0][0] = (false, 0);
  let mut frontline = HashSet::<(usize, usize, usize, usize)>::with_capacity(100);
  frontline.insert((0, 0, 0, 0));
  let destination = (width - 1, width - 1, 4, 4);
  while !frontline.is_empty() {
    let coords@(i, j, k, m) = *frontline.iter()
      .min_by_key(|(i, j, k, m)| dist_map[*i * width + *j][*k][*m].1)
      .unwrap();
    frontline.remove(&coords);
    let pos = i * width + j;
    dist_map[pos][k][m].0 = true;
    if coords == destination { break; }
    for coordsp@(ip, jp, kp, mp) in neighbors(i, j, k, m) {
      let posp = ip * width + jp;
      if !dist_map[posp][kp][mp].0 {
        dist_map[posp][kp][mp].1 = dist_map[posp][kp][mp].1
          .min(dist_map[pos][k][m].1 + risk(map[posp], kp, mp));
        frontline.insert(coordsp);
      }
    }
  }
  dist_map[map.len() - 1][4][4].1
}

pub fn main() {
  let (map, width) = input();
  println!("{}", dijkstra(&map, width));
}
