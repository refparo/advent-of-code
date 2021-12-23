use super::day23::*;

impl NewBurrow for Burrow<4> {
  fn new(side_rooms_in: [(u32, u32); 4]) -> Self {
    let mut side_rooms = [[0, 0, 0, 0]; 4];
    for i in 0..4 {
      side_rooms[i][0] = side_rooms_in[i].0;
      side_rooms[i][3] = side_rooms_in[i].1;
    }
    side_rooms[0][1] = 1000; side_rooms[0][2] = 1000;
    side_rooms[1][1] = 100;  side_rooms[1][2] = 10;
    side_rooms[2][1] = 10;   side_rooms[2][2] = 1;
    side_rooms[3][1] = 1;    side_rooms[3][2] = 100;
    Self {
      cost: 0,
      side_rooms,
      hallway: [0; 7]
    }
  }
}

pub fn main() {
  let init = Burrow::<4>::new(input);
  println!("{}", init.solve().cost);
}
