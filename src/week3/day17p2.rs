use super::day17::*;

// we have known from part 1 that
// x_n = (v + v - n + 1) * n / 2
// x_max = (v + 1) * v / 2 (at n>=v)
// y_n = (w + w - n + 1) * n / 2
// y_max = (w + 1) * w / 2 at n=w or w+1
// y=0 at n=2*w+1
// v_min = ceil(sqrt(2 * left - 1/4) - 1/2)
// w_max = - bottom - 1
//
// similarly,
// we should have x_1 = v <= right
// => v_max = right
// y_1 = w >= bottom
// => w_min = bottom
// this is not a big search space
// size = (right - ceil(sqrt(2 * left - 1/4) - 1/2)) * bottom * 2
// so we can just brute-force

pub fn main() {
  let area@(left, right, bottom, _) = input();
  let v_max = right;
  let v_min = ((2.0 * left as f64 - 0.25).sqrt() - 0.5).ceil() as i16;
  let w_max = -bottom - 1;
  let w_min = bottom;
  let count = (v_min..=v_max)
    .map(|v| (w_min..=w_max)
      .filter(|w| test(area, (v, *w)))
      .count())
    .sum::<usize>();
  println!("{}", count);
}
