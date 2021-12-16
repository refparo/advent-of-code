use super::day16::*;

fn version_sum(packet: &Packet) -> usize {
  packet.version() as usize + match packet {
    Lit {..} => { 0 }
    Op { subpackets, .. } => {
      subpackets.iter().map(version_sum).sum()
    }
  }
}

pub fn main() {
  let bits = input();
  let packet = Packet::from(&bits);
  println!("{}", version_sum(&packet));
}
