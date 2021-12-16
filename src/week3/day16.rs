use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn input() -> Vec<bool> {
  let file = File::open("input/day16.txt").unwrap();
  let hexs = BufReader::new(file).lines().next().unwrap().unwrap();
  let mut bits = Vec::with_capacity(hexs.len() * 4);
  for c in hexs.chars() {
    let num = c.to_digit(16).unwrap();
    bits.push(num & 8 != 0);
    bits.push(num & 4 != 0);
    bits.push(num & 2 != 0);
    bits.push(num & 1 != 0);
  }
  bits
}

#[derive(Debug)]
pub enum Packet {
  // VVV100(1NNNN)*0NNNN0*
  Lit {
    version: u8, // V
    value: u128 // N
  },
  // VVVTTT(0L{15}|1L{11})P+0*
  Op {
    version: u8, // V
    typeid: u8, // T != 100
    subpackets: Vec<Packet> // P
  }
}
pub use Packet::*;

impl Packet {
  pub fn from(bits: &[bool]) -> Packet {
    fn number<'a, I: Iterator<Item = &'a bool>>(bits: &mut I, len: usize)
      -> u8 {
      let mut res = 0;
      for _ in 0..len {
        res <<= 1;
        if *bits.next().unwrap() { res |= 1; }
      }
      res
    }
    fn packet<'a, I: Iterator<Item = &'a bool>>(bits: &mut I)
      -> (Packet, usize) {
      let version = number(bits, 3);
      let typeid = number(bits, 3);
      let mut packlen = 6;
      if typeid == 4 {
        let mut value = 0u128;
        while let Some(true) = bits.next() {
          value <<= 4;
          value |= number(bits, 4) as u128;
          packlen += 5;
        }
        value <<= 4;
        value |= number(bits, 4) as u128;
        packlen += 5;
        (Lit { version, value }, packlen)
      } else {
        if let Some(true) = bits.next() {
          let subnum = ((number(bits, 3) as u16) << 8)
            | ((number(bits, 4) as u16) << 4)
            | number(bits, 4) as u16;
          packlen += 12;
          let subpackets = (0..subnum).map(|_| {
            let (packet, len) = packet(bits);
            packlen += len;
            packet
          }).collect();
          (Op { version, typeid, subpackets }, packlen)
        } else {
          let mut sublen = ((number(bits, 3) as usize) << 12)
            | ((number(bits, 4) as usize) << 8)
            | ((number(bits, 4) as usize) << 4)
            | number(bits, 4) as usize;
          packlen += 16 + sublen;
          let mut subpackets = Vec::with_capacity(4);
          while sublen > 0 {
            let (packet, len) = packet(bits);
            subpackets.push(packet);
            sublen -= len;
          }
          (Op { version, typeid, subpackets }, packlen)
        }
      }  
    }
    let mut bits = bits.iter();
    packet(&mut bits).0
  }

  pub fn version(&self) -> u8 {
    match self {
      Lit { version, .. } => { *version }
      Op { version, .. } => { *version }
    }
  }
}
