use super::day23::*;

impl NewBurrow for Burrow<2> {
  fn new(side_rooms_in: [(u32, u32); 4]) -> Self {
    let mut side_rooms = [[0, 0]; 4];
    for i in 0..4 {
      side_rooms[i] = [side_rooms_in[i].0, side_rooms_in[i].1];
    }
    Self {
      cost: 0,
      side_rooms,
      hallway: [0; 7]
    }
  }
}

pub fn main() {
  let init = Burrow::<2>::new(input);
  println!("{}", init.solve().cost);
}
