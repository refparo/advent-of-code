use super::day22::*;

pub fn main() {
  let instr = input();
  let reactor = reboot(instr);
  println!("{}", count(&reactor));
}
