use super::day22::*;

pub fn main() {
  let instr = input().take_while(|&(_, ((x1, x2), (y1, y2), (z1, z2)))| {
    x1 >= -50 && x2 <= 51 && y1 >= -50 && y2 <= 51 && z1 >= -50 && z2 <= 51
  });
  let reactor = reboot(instr);
  println!("{}", count(&reactor));
}
