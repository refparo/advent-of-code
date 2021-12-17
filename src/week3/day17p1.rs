use super::day17::*;

// x_n = (v + v - n + 1) * n / 2
// x_max = (v + 1) * v / 2 (at n>=v)
// to make x_max >= left:
// v_min = ceil(sqrt(2 * left - 1/4) - 1/2)
// have v=v_min and probe will reach target at n>=v
//
// y_n = (w + w - n + 1) * n / 2
// y_max = (w + 1) * w / 2 at n=w or w+1
// and y=0 at n=2*w+1
// so we need top >= y_(2*w+2) = -w-1 >= bottom
// => -top-1 <= w <= -bottom-1
// and probe will reach target at n=2*w+2
//
// to reach max y
// we need w=-bottom-1
// and v=ceil(sqrt(2 * left - 1/4) - 1/2)<=n=2*w+2=-2*bottom and n=2*w+2
// fortunately, our data satisfies this quality
//
// so, y_max = (w + 1) * w / 2 = bottom * (bottom + 1) / 2

pub fn main() {
  let area@(left, _, bottom, _) = input();
  let v = ((2.0 * left as f64 - 0.25).sqrt() - 0.5).ceil() as i16;
  let w = -bottom - 1;
  assert!(test(area, (v, w)));
  println!("{}", bottom * (bottom + 1) / 2);
}
