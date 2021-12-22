pub fn input() -> (i16, i16, i16, i16) {
  if false {
    (20, 30, -10, -5)
  } else {
    (94, 151, -156, -103)
  }
}

pub fn test((left, right, bottom, top): (i16, i16, i16, i16),
  (v, w): (i16, i16)) -> bool {
  for n in 1.. {
    let x = if n <= v { (2 * v - n + 1) * n / 2 } else { (v + 1) * v / 2 };
    let y = (2 * w - n + 1) * n / 2;
    if x >= left && x <= right && y >= bottom && y <= top {
      return true;
    }
    if x > right || y < bottom {
      return false;
    }
  }
  unreachable!();
}
