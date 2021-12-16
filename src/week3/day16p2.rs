use super::day16::*;

fn calculate(packet: &Packet) -> u128 {
  match packet {
    Lit { value, .. } => { *value }
    Op { typeid, subpackets, .. } => {
      let mut iter = subpackets.iter().map(calculate);
      match typeid {
        0 => { iter.sum() }
        1 => { iter.product() }
        2 => { iter.min().unwrap() }
        3 => { iter.max().unwrap() }
        5 => { (iter.next().unwrap() > iter.next().unwrap()) as u128 }
        6 => { (iter.next().unwrap() < iter.next().unwrap()) as u128 }
        7 => { (iter.next().unwrap() == iter.next().unwrap()) as u128 }
        _ => { panic!(); }
      }
    }
  }
}

pub fn main() {
  let bits = input();
  let packet = Packet::from(&bits);
  println!("{}", calculate(&packet));
}
