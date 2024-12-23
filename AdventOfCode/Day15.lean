import AdventOfCode.Utils

namespace Day15

inductive Tile where
| wall | space | box | leftHalfBox | rightHalfBox | robot
deriving Inhabited, BEq

instance : ToString Tile where
  toString
  | .wall => "#"
  | .space => "."
  | .box => "O"
  | .leftHalfBox => "["
  | .rightHalfBox => "]"
  | .robot => "@"

def parseInput (input : String) :=
  match input.splitOn "\n\n" with
  | [grid, moves] =>
    let (mat, robot) := StateT.run (m := Id) (s := Option.none)
      $ Matrix.parseM! grid fun (i, j) => fun
        | '#' => pure Tile.wall
        | '.' => pure .space
        | 'O' => pure .box
        | '@' => do
          StateT.set $ Option.some (i, j)
          pure .robot
        | _ => panic!"illegal input"
    let moves := moves.foldl (init := #[])
      fun (moves : Array (Offset × Offset)) => fun
      | '^' => moves.push (-1o, 0)
      | 'v' => moves.push (1o, 0)
      | '<' => moves.push (0, -1o)
      | '>' => moves.push (0, 1o)
      | _ => moves
    (mat, robot.get!, moves)
  | _ => panic!"illegal input"

partial def step
  (mat : Matrix Tile) (pos : Nat × Nat)
  (move : Offset × Offset)
:=
  let target := pos + move
  match mat[target]! with
  | .space => (mat.swap! pos target, target)
  | .wall => (mat, pos)
  | .box =>
    let (mat, target') := step mat target move
    if target' != target then
      (mat.swap! pos target, target)
    else
      (mat, pos)
  | .leftHalfBox | .rightHalfBox => panic!"unsupported operation"
  | .robot => panic!"hello, another robot!"

def widen (mat : Matrix Tile) : Matrix Tile where
  array := mat.array.foldl (init := Array.mkEmpty $ mat.array.size * 2)
    fun mat => fun
    | .space => mat.push .space |>.push .space
    | .wall => mat.push .wall |>.push .wall
    | .box => mat.push .leftHalfBox |>.push .rightHalfBox
    | .robot => mat.push .robot |>.push .space
    | .leftHalfBox | .rightHalfBox => panic!"wide boxes can't be widened"
  width := mat.width * 2

partial def wideStep
  (mat : Matrix Tile) (pos's : Array (Nat × Nat))
  (move : Offset × Offset)
:= Id.run do
  let mut boxes := #[]
  for pos in pos's do
    let target := pos + move
    match mat[target]! with
    | .space => ()
    | .wall => return (mat, false)
    | .box => boxes := boxes.push target
    | .leftHalfBox =>
      if move.snd == 0 then
        let otherHalf := target + (0, 1)
        if ! boxes.contains otherHalf then boxes := boxes.push otherHalf
        if ! boxes.contains target then boxes := boxes.push target
      else boxes := boxes.push target
    | .rightHalfBox =>
      if move.snd == 0 then
        let otherHalf := target + (0, -1o)
        if ! boxes.contains otherHalf then boxes := boxes.push otherHalf
        if ! boxes.contains target then boxes := boxes.push target
      else boxes := boxes.push target
    | .robot => panic!"hello, another robot!"
  let mat <- if boxes.size > 0 then
    let (mat, success) <- wideStep mat boxes move
    if ! success then return (mat, false)
    mat
  else mat
  let mat := pos's.foldl (init := mat) fun mat pos => Matrix.swap! mat pos (pos + move)
  (mat, true)

def gps (mat : Matrix Tile) :=
  (0, mat.height).foldI (a := 0) fun i total =>
    (0, mat.width).foldI (a := total) fun j total =>
      let tile := mat[(i, j)]!
      total + if tile == .box || tile == .leftHalfBox then 100 * i + j else 0

def solvePart1 : Matrix Tile × (Nat × Nat) × Array (Offset × Offset) -> Nat
| (mat, robot, moves) =>
  gps $ Prod.fst $ moves.foldl (init := (mat, robot)) $ uncurry step

def solvePart2 : Matrix Tile × (Nat × Nat) × Array (Offset × Offset) -> Nat
| (mat, robot, moves) =>
  let mat := widen mat
  let robot := (robot.fst, robot.snd * 2)
  gps $ Prod.fst $ moves.foldl (init := (mat, robot)) fun (mat, robot) move =>
    let (mat, success) := wideStep mat #[robot] move
    (mat, if success then robot + move else robot)

def input := parseInput "\
##################################################
#.....O..O....O.#.OOO...#....#....OO......OOOO...#
#O......OOO..#..O...O.#........O.OOOO.OOO........#
#..#..O.O..O.......O....#..O.O..O.O#...OOO....O..#
#.......O..O..O.O.#..#......O#..OO...#..##..O.O..#
#.#...O....O......O...O#.OO.....OO..#.O..O.......#
#OOO.O....OOOOOOOO.O...O..O.O..O.........O....O.O#
#.O...#.##.#.....O.O.O...........O....OOO#OO..O..#
#.OO.O.O.....O.#OO......O.O#.O.O........OO.O.....#
#...O....#OOO.OOO.O#.........OO#.O....O.O..O.OO..#
##O#O#.....O..O..#...O.........O.O....O..#OO#..#O#
#.OO.O.....#.O.#.O....O...O...O..O....O##O..O#O..#
#.O..O.O......OO.#..O...O.O..#....#...O.O#.##..#.#
#......O....#O..O.....O.......O..O....OO..#..O..O#
#.#.O....O..#O.O...O.#...O..#..........OO...O....#
#OOO...#O....O..O..OOO..O......#O..O#O.....O..O..#
#......O......O..#.....O.....OOOO...OO.OOO.O.....#
#.O.O..O.O..#.....#OO..OO.#O..OO..O.O#O....O..#..#
#.O.OOO..O..OO.........O...OOO...#..OO.O.O.....#O#
#.......OO..O...OO......OO.......O.O.O..#..##.O.##
#O..O.O...#...OO....OO.....O...OOO...#O..O.O.....#
#..#.O.#O..OO.OO..O..#OO#..OOO.....O....OO.O....O#
#O...O..O#..###..#OOOO.O.O.O.O.....#OOO....O.OOO.#
#....O.OO.#..#........OO......O.#..O.O.O.........#
#.O.O#O....O....O#..O.#.@.....O..OO.......OO..OOO#
#OOO........#..OO#....#.O.O..#..O#..............O#
#..O.OO.O.O.O#.OO.OO#OO.O....OOO.#O.O...OOO..O#..#
#..........O..O.....O..O......O......#OO.OO..O...#
#....O.O...O...O.O.O.OO.#O.......#O.O...O....O...#
#......O..OO......##....O#O....#.O.....#..#.O...O#
#..O...O...O..O.#.....#OO..O.O#..O....O.O.....O..#
#OO.....O..O.....OO...#........O.O#O..OO..O....O.#
#.OOO..O...O....#...O#O.O.O.#...O.O.....O..OO...O#
#.O..O......O..#..O.......#.OO..O.O........#.....#
#...O.O.O..OO..OO.#.O..O...........OO....O.OOO.###
#O....#..#..#.....OO..O..OO....O......O..O#......#
#...O.O........O..#.O.O#.....O.O.O.O..O..#.O.O..O#
#...OO..O.....O............#.....O.O.O.....OO..O.#
#OO#O.O.O#..#.#..O.#....##.OOO......O..O.#...O...#
#..OO....O.......O.....O#...O.......OO#O...O...O.#
#.#.OO.....#OOO..#.......O.O.O....O..............#
#O........#.O.OO....OOO..O.......#.OO.O.O....#...#
##O........O.O..#.....OO#O.O.OOOO.#...OOO.#O#O#.##
#..O....O.#OO....OOO.##.#O..O..O..#O.O..OO.......#
#O...#..#O.O.OO..##.O.O..O......O.O.O...#OO.##O.##
##..............OO...O..O........#.....O..OO..O..#
#.O.#O.OO...OO.O.O.O..OOO....O.O.O...OO.O....#..##
##O.....O#....#O#..O##......##.#OOOO.#.OO.O.OOO..#
##.O......#........OO#.O..#.#..O.O.OO.#.O..O#.O.##
##################################################

<vv^><<vv>v>v>^^><>><<^vv>^v>^>^>>>^><>^vv^v><v<^><>><v^^^v>^>>>^^^^>>^v^>^v>vvv<<<<>v><^<^<><><><v><><<<^>><><>v<>^>><<<v^vv><^<<^v>>^v^^<<<>>vv^^^^<<^>>^v^><<v<<><>^<vv<<v<^<<>^<vvv>^><>vv^^v>><v>^^^>v^<v^<^<v>v^vv<^<v>><^vv<^><<v^^<<^><vv^v>v<><^<>v<v^<v^>v><<^>^^^<><<><v<vvv^>^vvv^><v<<v<><<^<v><v>^>><^v>><>^v<^^v^^<v<><^>>^^vv>>^^^<^v><<^^^>^^><^>vv<><<v<>>^v^<<^><^v^^v><<v><><><vv<^<v<>v<<<<>vv<>^<<<v>v>>><<<^v>>^^>vv><vv<<v>^vv^v<^><v<<^<<^<>>^v>>^vvv^<>v<^^^<<v>vvv>vv^^<vv<<^>v<<><>>^>v>>vv<<^vv^^^<<v>^^<^^^^^vv><>^vv>^v^^<<>>>^v^v>^^^<<><vv>v><v^^^^<<^>>^<>v^v<^^<v>^^<><><><^^>>v<v>^>^><^><v><<<<vvv^><^^^v>^^<^^v>^>v>>v>>>v^<^>vv<>^v>>>^>vv^>v^<>v><^><<v<v><><<<vvvv>v>^^vv<>>v^^v>v^^<^>>><>>vv>^<vv^><><><<<vv<>v<^v>>v<v<v<^<v><^vv<vv<^>^<vv><v>>v>>^>^v<><<^v>^^>v^v<^^^>^vv>^^<<v>^v>><^>^>^<>^^<^^<v>v<<>^>>^v<v^v>v<>v^^>^<v<v>vvvv><>>^^>>^<v<v^>>^v^<v>^v^^^^<^<vv^><>vvv<v>^<vvvv^>^^^^>^^^^^>v^v>v>>v^><<v<<<^^vv>><<v>^>>^<^>>v^<<v<^vv>vv>v<<^<>v^>>><v><v^v^v<v<v^>^^^v>v>^^v^^>v<
v>>^v<^><^><<>>><>>v^<<<>^^<<^^><><>vv<^<^^^<<^<v<><<<vvv<v^^v>^v>v<<>v<v>v^^><v>^v^^<v^^^<vvv><<^<v>v^^v>>>^^<v^v><<<>^^>^>v<v^<vv^>^<<^vv>>v^>v^v<<<v^v<v>^>v<<vv<^^<^v><>^<>v^v>>^v<v^v^^v^>^>^>>vv><^<vv>><vvv<v^<vv<>vv^vv^^<>vv>^^<<<<v^>v>^^><><v<vv^v^^<<vv>^^<^<<^<>^<<vvv^^v<<><v><>^>>v^vv^v>><v<v<<<^^^^^<><^<><><^<<<>^v^v><^<^^^^v^<v^>^v^<v^^<<>>>^^v>><>>>><<vvv^<v>^v>>>v<^^<<^^><>^^>>^<^<>>^v><v<<<v>>>v>^^<^>>^><^v>>v><<v<v<^^<v<^^v>^^<><><>vv^^^<v^<v^^vv<vv^^<<v>>^^v>>v><><<v^v>^>><><^>^^^<^^v<>^v^<<>>vvv<<^<v^v><<>^<v<>>v<v^^vv>^>>vv<<^<<v>v^v<v>vvv^<<<>^<vvv<>^^vv<^<^^<v^>>>><<^>>^^^>^v><v<^^<>>>>v^v<<vv>>^vvv<^vv<<v^^<^^<v>>^<<v>^>>^>vv^v<>>^<v>^>>^v<>><^>>>><<<>^v^^v>v<^v^^vvv<<>^><<v<<v^v>v><>^v<<^^^vv<<<<<<vv<v^^>v<<vv^<<v>v^v<<v>vvv^<vvv>v<v<>v<<v<v>>>^>^^v^<><<<>^<><>^>^>^>><>>><v<^<v<v<><<>^>^v<^^<>>^^<^<<><<<<<^^v><<^<v^v^<<^v^<<^>^>><^>^v<v<^v^>vv<>v<>>>v^^^>^v<vvv^^<^<vvv<^<>>><v<v><v<^<vvvv><^<<v<<^<<<^v^>v<>^v<^>>^>^>v>^^<><v>^<><<^<<<<<<>^v>>^><<><^^>>^vvv>^v>v>^<<
>><^<>><>vv^v<v>^>vvv>^<<<<><>v>v^<v><<>v^>>^^^^<^v><vv<<<><<^<v>>v^<vv^>^<v>^<v<<v>>vv<v^^v>^>v^v<<>>vv^><v<<>>^><><<^v><v^^^<v>vv<<<>^<<v>vvv^v<<^^v^^^><<^<vv<><^>v<^>^<<^v^<vv><v>>v<>^<<vv<^<v>^>v<^<>>^v<^><>><^^^v<<v>>v>^>^>>v<<><^v^>^<^>^<>^>^^>vv><<vv^>>>^<>^vv^v^<v>^>v^>>^><vvv^v<v<>vv^>^><v>^vv>^vv<>^<vv><<v<v^v>vvv><^v<><>^^^^v^^v^<v^<^v<>^v>>^v^v>vv<^<>><><vv<v^^>v<vv^^^^^^v>>><v>vvv^vv>^<^<>v^<^^<^<<<<>><<<v><>vv^>v^<>^^<>>>v<>v<<><v^<<^vv><<v>>>^v<>v^<>v^v>v<v^vv>^^><<^v>vv^v>><v><v<v<vv<<><^^<v^vv^^<<>v<<v<vv>>^^<<^<^><v<<<^<^>^>>^^<>^^v>^>^><^<<<<>v^>>><^v^v<v>^<^^<>>v<^>v^^<vvv<^v>>v<><vv>^^vv>>^<^v^^^v>><^<^^<vv<<vv^^<v><v^v>vv>^v<^^>v>v^vv^v<^<>^<<>v>>><<<<>>>>vv>><<v<vv><v>><>>v^<^v><^^^<>>^>>vv^><^>vv<<v<><^^>^><<vv<<>>v^<^<^<^<vvv^<>^><<<^>>v<>^>v<<><vv<<>^^v^vvv>^>vv^<>v<^>v<^<v<^><<v<>>^v>v^<<v><>^<^<>v^<^^<^>^^>^<>v>v<v^^^>v>>>v^>>vv>>v><v>v>^^^<v>>^v^^^<>><<v>^vv<^vv^^^^^>><<v>^^<<v^v>v<>>vv>v<>^^v>^>^<<^^^^<v>v^v^<<<v<^>^^>^<v<v^<^<v<><<><v^<^v^^^^v^<^<^v<vv>v>
v<^^<>v^v<><<^^<v^>><<>>v<vv^vvv>v<>^>><>><v^<v>^>v>v^v<><v<<<<<<v^v^<<>vv<v^<^<>^<<^^vv<v<>>^^v<<vv^>v^>^><>^v>^^>^v^<><>v<<^>>v<v^<^<<><<^><<<<^v>>v^v<>v>v>>v>><vvv^v>^^^^<>^<v><>vv^<>^v>^<>>>>^<v<>>><v<^><v<^^<<<<v^>>>^<v<^^>^<^^<><<^>v^v>^^>><<<<v><^^^>>v^>><^^<<vv>>v<>v^^^v<^v><<^v>vv^vv<^>>>^vv^>v<>^<>v><^>^v><<><>v>^><v>^<v><vv^^^>v^^^>v^<vvv^v<v^vvv^v>^^^<v>><v^>>v>^>^v>v<^^^>^>>v^>^v>v^^^^<v^v<v^^v><<<v<v>v^^>v<><v^>>v^^^^>^<v<>>><^v<><v^^^^^>v^^^><>>^<^v<v^<>v>>v<>><vv>><><^<>v<<^v^vv<v<><v>>v^^^<>^>^^>>>v>>^<v>^>^^v>>>>v>><>>>^v^<v<>^^><<^^v^<<^<^<><<v^v<<>^^^<^<>v^^<<>v^<>>><v^>>>>><^>^^vvv<>v<v<>vv>v><^><<<><<vv<^>^v<<><>>>>^^>v>^^<v><>>>v<<>><>v^vv<^^v<vvv><<>^<><vv^<^>vvvvv<<v<v<>^^v>v^vvvv<><<<v>v<^>v>>>>^>^>v>>v^>><^vv>^^<v>vvvv<>v<^^>>^<<><<<^<<vv<<vvv^>>>v<<>><<vv^v><>v<>>^><^<vv^^>v<v><v<>^<^v^<><v^<v<<>><^vv<<v>><<^<v<>>^<^>^^>>v^v><v^v<^^^v>vv>^^<><v^<v>v>v><<^^<v<v<^><>><^><><^>^^v<^^<^<><v>>>v<vvvv^<<>><v^<<<<^v>v><vv<^^<<^^>v>>vv>^^v>^vvv<v^>^v<>>>vv<v<<<>v><<<
v<^<^<<vv^<^>v^>^^>>^^><<^<>v>^>v<^>^vv<^>v>>><<^v>^^^<<<<v^<vv^^><>v>v^vv>v><<<<><v<<v<^><<v>>>><^v>>vvv<<<^><<v<<<^><^v>^v^v^>^<<v>^^<^>^<>v^><<>vv<^<^<<v<<>^^^>^v^>>>^><<<^v<vv^^>v^^><^^>><<^<^^^vv^v><>>^v^<^v<><>v^><>v>v<>^>><^^>v<<v^>v>vv^<<<^>^<vv^^v<v^<<><vv<<^>^v<>v^v<><><><v>^>>^><^v>>><<v<>^^>^^^v<>^<v>v<><><>>>v<^<<<<v^^^^v<vv^^<<<<v>^^v>><v>>v<<<^vvv<>^<vv^vvvvvvv<>>>>v><^>><^><vv>>><>>>>^v^<^^><>^><>>>><vv^^>v>>>>>v^vv^<v^><>^>><^<^<v><><<>v^<vv>vvv<^<>>v<<^^>>^<>^^vv<v^v<vvv^>>><v<v<v^v>vv><^<><>^<v<<v<^vvv<vv>v>>v>^<<>^<>^^v<>>^v>v^v><><^><v^>vv>>^<<v^v<<<v<^<^v^<^<><^^^>>>v^v>v<^><><<^>^<^v^<><^v<v<>>v<<^^<>^<vv>v<<v^v^vvvvv^v>^><vv>vv<<^^vv>>^vv<<^>>^^^>><>vvv<>^>v><<<>^v^><^>^<<^^v^<<v>v<v>><><<v><^>><<^<^<<>>vv<<^vv>^^<<^<>^^<^v<v^v<^<><>>vvv><<>^>vv><v>>>v<<<>v>vvv<><><vvv<><vv^<v^^><<>^v<v<<<^<<<><>>>^^<^v<v<>v^<<v><<^<>v<>v<>^v<<<>^vv^>>^^v>v<^v<^<v<v^^><^^<<^<v><<v^>>v^>v^<v^^^v>^^>v<^vvv<v<v<<>>v^>v<^^>>^v<<^>vv<vvv><<v<v^^^<vv<v^><<v<^<^v>v<^v^>v<<>>>><>^^v^>>>
vvvvv>vvv^vv<^>^v>><><>v^^v>^v^<<<^>>>vv>^>^<v>v>v<<^v<<v>><><<^v<^^v<^^^^^>v>^>v^v^^<^v^<v><<<<^>>>v<<<^vv^<^>>>v<^>^v<^<v><<^>vv<>>>^v>v>^>^<>^^><>^^v<v<^>v><v>>^vv^>vv^><v><>^><<^<v<>^^^vv>v^v^v<v^vvv>>>vv^vvvv^>>v^^<^<>v>v<<v<>^<^<^>v<>>^>v>^^<^v><>^<><>v^><>><^vv^>vv>>>^<vv<>>v>v<vv^vv><^vv^<^^<<^v<<>>^>v><vv<<^v<>v<^v><^>^<<v><v>vv<^<<<^<>^>>v>>>>>>v^<<vvv^<<v^<v><<v>>^<^><^>v^<><>>^<^^<^<>vv^>^>v><<<<v><vvv><^>^><>^^v><^^v><v^v>^<<^^^v<<>^>^vv<v^vv^v>><vv>>^<<^v<v<>vvv^<^v>>>^<v^v<vv>^v^><>v>v>>v>vv<^<^v>^<<>v^>>v>v<<<vvv>>v<>><<<<v^<<v>><<>>>^<>><^<v>^^^>^^^v^><<>>><^v<>>^>>^v><<^^<v<v<>v^^<><^^>>>vv^>v>>v^<>>>>vv>><v<^<^<^^^v>>v>v>vv^>>^^^><v^<^^<<>v>^>><>>^^vvv><>v>v^^>v^v<<v^v<<>>><>^>>v^>v^v^v^<<<^<><v<v><v^^<vv><<v<^v^>^^>>vvv>v><>^<v>v>>v<<><v^>><^v<<v>^^>v^^v^>vv<^><>>><v<v<><^<v<<>>^<<v>vv>^<v>vv>v><<vv>^>^v<^>>^v<<v<v><<v<><^^^^><^<^>v<^<^>>v<<^>^<v>v>^^^>^^>^^><v><v^><<^^^<>v<<^<^v^v><<>^^vv>^<<<<><<>>^^^<^vv^v><>v<<^>v^^^vv^^^v>>^^vv>>^^<^^^v>>>vv<^<vv>^<><>>vv>v<<<>
^^>^>><<<v<<>>>^^>v^<v<>v<<v<<<v<>>^>><v<>>^^^v>><<>>>><^^vv^>vv<<v^^v<<v<^>v<v^v<^>^^^v>v^v<v>>^v<^^v>v>v>>^<v<<v>v^>^>^^<v^vv>>>v^<^v<^^^>>v<vvv<^<^<^v<^>vvv<>vv<><v>v^<^^v^^vv<>>vv<v<><v><>vv><vv<<^><^<<<><<v<>^v<><^^v>>^>^^^>>^v>^v<>>^>vv<^^^^<><><><<^^^<^><^<v^v^v^^vv>v^^v>>>^<>>><<^^>^<<^<v><>>^^^>v<v<v<>><>><><>>^^v<<^^v>vvvvvv><v<<<^>^<^><<>>v^v^>v<^^<><vv<v<v<<><><vv^v^^v<^^v>^v^^<^>v^>v<v^vvv<^>vv^>>><v>>^v>>>^<v<v^^v<^<^^<<v><vv^>vv<v>v^v><^^>^^<^v<vv<>><vv^<>>^>>>^>>>><>><<^^<vv><v^<><<v<<vv^^v><<^<^<<vv^v<<<<<v^>^<>vv<>^vv^>>^>vvvv<<<vv<^v<v^^^^v>><<v>^v><v<>>v<^v<v^>><^^^v>v^v^vv>>v^><<^v<^v<<>><v>><v<v<>>><vv^<v>v^v<^<>>v<>v^vv^><>><v<vv<<v><>v<<<v^<><^>v<v><>vv^>>vvvv><<><>v>v^><<^<^>^<<vv<v>^^>v<vv>>vv>v<vv^>vv<<^v^vv<>v<vvv><^vv^vv^<<<^<v^vvv>>>>v<v><^>v^>vv<vv<v<<v<<v<v>^v<<v<^<^>^vv>><>>>^v>vv>>^<v<<<<^^><^>v><>><<>^<<<v^<v^<^<^>^^<v<>v>>v<^<v^><v>^>v^^^^><<><^<>>v^vvv<v<^<>^<v>v<<<vvv<v<<^<<<>^<v<^><><^<^><v^>v^v><^<v^<^>><v<>v^>v<v><^vv^<>^vv>v>><v<<>v^vv^<<><^vv^
^><^^^^>v<^<>^>v>^^^^v^>v><vv^vv<>v<^v<^<>^><><^^><v<^<v>>^^>^<<<<^<v>>^<^><^<><^^><v>v^>><<>v>^^^><<<^^<>^<^^^>^v><<^^<^><<^^>v>^<^<^^<>^^<^>^><>v<<<<v>^<<^v^><v>v<>^>v<^^vv^><<>^<^vv>vv^^v^<v<^vv>^>^^<>^^vv<<v>^^^<<^<<v<<<vvv<vv<<^<<^^^>^^^^^<vv<^vv<>^<v<<>><^<>>>^^>^v<>v<v>^><>v<^v^<>^v^^<><<v^^<v>^^>>^v<>>^<>^v^><v><^^<v^>>^v^<<^<<v^>>^<^>><^><^^><>>>>vv^><^>>^v<v^>vv>>>>><v^v<<>v><<>>vv^^>^>><<v>>^^v<<v^<v>>^<<^>^><v>^<^>v^v<>^<<v<v^>>>^>v<><<v>>>v^>v<<<^<<v><v><vv>>>>v^<<^v>^<<v<>>>>>>v<<vvvvv<>^v<>^<<<^v<>>>^^^^>v^^^^<v<<^<^><>^v^^<v>><^^^<vv>^<<><><><>vvv>^>v^^>^>><<^<v><>vvv^v^^<>v><^^v<v>>v^><>><^v>^<<<^^<vv^<><vv^><^^<vv>><^vv><^>vv>v^<>^>vv^v^<>^<<v^^v>vv<^<v><<^<><>^v>^>^^<>><<^<v^^^^^><vv^><>v^<>v><<<v^><<<^v^>vv><v><v^^^><>>><>v^^>><>>^>v>>>>>v<<^^v><<v^<v^v>^<vv^><>v><v><vv<>v>>>^^v>v^>v^<^^^v<v<v<v^^^v>vvv>>><v^<^><>><<<>><<v^^<><<^v>>^v><><^>><^^^<v<^^><vv^<v<v<v^v>>v>vv>^v>v<>^<v><<^^vv^^^<^v<v<v<<<>^<>v^^>>^<<^^^^<v><^v>v<v<<^v<<vv^^^<<>v<^>>vv<><<<>v<^<<^^>>v^>v>^^
v^v<^>v^v^>^^<v>>^v<<v^vv>v<><^v><><v<^<v^v<>v^<^v>>>v>^vv<<^<vv^^<>^>v<^^>v^^<v<v>^<><>^>^^^>^^^>v^<<v<v^v^^<<>v>vv>><^^><>vv^^<v<v>v><<v>vvv>^<><^<v^^>^>>^vvv<vvv>v^^<<>v>vv<^<<<<>>vv^<vv^>^v>vv<v^v<v^^^vv^^vvv^<^^>^<vvv<v<^<^>>vv<><<v>^<v<v^v^<>^<vv<><^^v<>^^^<<v>v<>v<>v<<<<<>><<^<>v^>v>^>^>^^<^><><>^<^v<>^>vv<^<^<>v>vv^<v^<><>v>>><v^v<>v^vv<>v>^><<v<v^>^>><^^vvv<<<<>v><>v>vvv>v^vv<>v^v<<><<vvv^^<<>^>>^^>v>^v^>>>^v<>^<^^><v^<>^<>^>>>^<<<>vv>v<^^vv<v^vv<>><v<>>^>^^v>^<v><>^v>^^>^<<^^^^<><^><<v>^^>v^vv^>^v><>>v>^v^^>^<^^>v<^v^v><><<v^>vv^^^>>^><>^vv<>^<^<<vvv^<<>>vv>^^<<^<>v<^<v<>^^><<<^<^<^v^<^<>v^>>>><^v>v>^v^<>^><^^>><><vv>vvvv^>vvvv^v<<><v^vv^^>><<vv^>^^>><>>^v>>>^>>^^>^>^<<>>><v<^<v<vvv^><<>v<<^v>>vvv^v<^vv^v>v>>^>^>^>>vvv^<><><>^v^<<<^>>>v^<^<^<<><<><<^<v><<v<^<<>>><<v^>>>>^v<v><<v>v>^vv^<<vv<v^<>^v><<<><^v^^>v<v^><vvv><v^v><<^^>v<>^^^v^^>^^v<v<v<<^<^>v>>^^<<>v^^^^v<>>^^vv<<>>vv^^<^<<^>v^^v<v<>>v^>>v<^>>><>v^>v<>>>^<<vv^>v<<><><vv>^v^>>v<>v<^>v><>^<>vvv<>^<v^<<^v^^vv>v>vv^v^<v><
<>^><>v^<<^^<>v><>^^^<^vvv>v<^v<v>^><>v>vv>v<<<<>v>><><vv^>>v<v<>>^<<><>v<>>>>><^^^^>^v><^<v<v<^v^vv<<>><>^<<>>^><^<v^v^><<<>v^><^v^vv>v><v><v^><><><^<<><<^vv<v^>v^v^v>v>v<vvvv>>>^^v^v<>v^^vv>><<<<<<>><^^^v^<vv>>>v^<><>^v<v<<<^v><v>^>^<<^<^<v<^<v^<v<<v><v^^^<vv>>^^^v^>>>>v>v>>>><^<>>^>><v<>>>v>>vv<<>^^><><><vv^v>>><<vvv<v><^<<^<v<^<<>v^^>v<vv<>v<>^v>^^<<><^vv><^><^<><v>>^>^v<vv<><>><<>^v><>v^<>><<><>v^^>^>v<<><v>v^vvv^<>^^>v<<<<><^<<v><><v^^^<v>v^<^^v<<>v<<vv><^<><v><>v>^<vv<^>><><>^<<<>vv^>^<^>^>^v^>^>v>vvv<v<v>^^>^v><^>>^^v^<<^><^^v<^^^v><v<>v^<><^^<v^><v<<v^><>^v^^vvv<>^<vv^^v><v<><<v^v>vv>v<<<<<>v><vv>>^^>v<vv^<^vvv>>vv<v>v<>v<>>>vvv<>^<v^<<v<^v^v^>><<^<>v>^<><<<<^^>v<^><v><v^<>v>>><^v>><<>v<><>v^^><>>v<>v>><^^v<^>>vv^>v^^>vv><>>>vv>v><v^^<^>^^^<v<>^^v<^v^v><^^v<^>^^><>v^^^^<^v^>^v^><v^<^<>^<vv^<>><<^v>v^<<>>^<^<<<><^><>>v^v><v>v>^>^^v>>^>>^^^^vv<>^^>>v>^vv<<<>>v^vv>>v^^^v<>v<^v^^v^^<^^<<<>^<<>^^^v^><>^^>^<v^><><v><^<>^^<v>^^>^>^^^v>vv>^><vv^v><><^<vv^^^><v<vv>>v>><<v<v<v<>v>>^>>^v
><<^<^<^>^^<>>^^>>^v^<><>vv^><<v<^>>^^v^<<^>v^v^<><<>^><v<v^^>><>>^>v<<>>>v><v>^^v>^<v>v^^>>>vvv>^v<>v<<>^<<v^>v^<>^v^^>><><>v>>>vv><v>vv^vvv>^^^<>>><^^^v<>v>^<^v>v^^vvvv^v>^^vv^^<<>><v<<v<^>^^<>^<<<v>v>^>^^v^>v^<^<>>v^<^v<vvv<v><>>^^><^vv<<<<>v^v><>^^><^vv><<<<^vv>vvv<>v^<<^>v^^v>v>^<<^>><^v^v<>v>>v>^vv>>v^><^^^^<<<>^^<v^^v<v<v>vvv>>^^<<^>^^<^v<<vv><>^<v<^v<^>v^^<>v^>>^^^v<>><v<v^^v^<v<v^v^>^>>^>^v<><>^vv><<v^^<>vv>vv<<vv^^^v^v^v<v<^><vv^>^>>><<>^><^>^>^^^<<v^>>>><<>>v^v<^<v^^v^^^<v<v^v^^>v>v><v^><>v>><>^^>><<^vv<<>^v<v>^<v^^v>^<^<^>vvvv^^v^>vv<<<<>^>>>><v^^^<<<>^>v^vvv><vv><>>v<^<^v>^<>>>vvvv>^vv^^^v>>^v>>^v<v>^>vv>v>>><vvvv<>>v>v<<>v^<<^<<^>>vv<^^<>v>^^vv^v^^^^vv><>>vv<>v^^>^vvv^^<^<^^v^^<vv<v<v>vv^^^^v^>><>><<v>^v<^^^>>v>v>v^^^^v><^>>v^<<v>>v<^<vv>vv<v^<>>^^^>^<>><vv>^<>>^^^<><^<^v^>>^v>>^v<^v^>><^><vvv^vv><<<vv>^^<>vv>>v<>>^><v^>v<<<<>v<>^>^<>v<v^><^^v<^><v>>^v^^>^<><>^>^><v>>>>>>vv^>^^><^v<^>>^<<>><<<v<v<^<<<^>>vv^>vvv<><>^>>>^v^^v^vv>v>><<^^>vv<<v><><v^><v>>>^^v<<>^<v<<>vvv><><v
^<>>vvv^<<^<v<>^<^<^>v>v>^<<<^^<^vvv^<^>v^^^vv>><>^vv>v^^v^vv><^^^><>>v<v>^><>^v<<v>><v>>^>>^v^>vvv><>v^<>>^<<^<>^>>v^<^<>^^^^<><v^v<v<^^>^>>^v>v>vv^<^<^v^>^v^<>vv<>^^<>^<^<^v^<^vv<^vvv^^^v<>^^vvv<v^^>v>^>v<^<^^^<>^<v>>><v^vvvv<>^>^v>v<><>^v<^^v><^<v<v<<^^^^<v<^>^^<vv><<^<<^>^<^vv>v^>^>><vvv><<^>>>^<>>v<v^<vv<<^<><<^^<^><^<>v^>^>^<^><v^<<^<vv><<<<^<v<<>^^v<>>v^v<<v^<<<><>^v>>>^^<v>>v^<v<v^<^^^v<<<><v<^>><^v^^>>><>>^<v^vv^v<v^<<v^<v><^^>vv<<<vv<<><<v>vv<v<>v^<<<v^v^v^>v<^<>>v^vv>v>v<<><>v<<<^vv^vv^>>>><v<>>^v^<>v>^<<>><<<^^<<>^v>^>>>v><<v>>vvv>>>^>>v><^^>^^^>^>^v^^v^>v^^^^<^v>v>^<v^vv>>><^><^vv^v<>^^><^v<<^<vv><<^^<<^<>>v^><v^><<v^^^^<v<^<>>v^^>^><<vv<<<v<>^>^>^v<<^>^<<^v^vvvv<vvv<<^>>v>v<^v>^>^v^>v^^v<<>><>v^^>^vv>v<>vv^><^>v^vv<><v<^v<>vv^<^>>>v<>v<><v>v><>^^><<>^^<^vvvv^v^v>v>v<<^><<>vv^<v<<v>^<^v^<vvv><^<<>v><<^^vv>^<>^>^^>v^^>v^>>>^v^^<^^>^<<^^<vv^^^v^<^<<^><^>v^>>^>^>v>vvvv^<<<>^<<v^>^v<<<v^vv><>v>>^^<><v<>>^>^>>>>v^<v^^v>v>^^vv^^<^v>v^v>v^^^>>>^^>>^^^v>>vv>^vv^^^^>>>v<^<<><v>^^>^
><v>^^vvv>><<^<>v>v><><<v^^>v><vvv^^>v<<>v<><v>^^<<^>><<>vv<<>vvv<v<<^>>><^<<v>^<vvv<<^^^vvvv><<v>^><vv<v^><^v>^v^>v><v^v^>>^><^>><v>^v^^>><<>v^>>v<v<v<v>v^^^v<>>v^<<vv>>>^<>^^>v>^<v>^v<<vvvv>>^v^<v<v><>^^>^v<v<<^^<>v^>^^>vv<<>^^><^^><<vv>>v>^^^<v>>v<^<^vvvvv><<^^^<^<<^<<<^<>>><^>>>>><v^<>v<<>v>^<<<^<<^vv><v^v<^><>><v<^>^vvv><v>v<><>>>vvv^<^v<v<^<<<v^>>^<v>>>^<><<^>v<>^v^<v<v<><v^><^^<^v><vvv^vvvv>^v<^>^<<^>>^v^<<^>>>><>vv<<^v^v^v<v<^>v>><v^<^<v<>^><^^<<^^^>v^v<^^v>><<>^vv><><>>v^<>>>^>v^^<v^^^>^v>>^v<^>v<>>v>v<v^^><>>><v>^vv<^v><v>vv>vv><v^<<<>>>^^>v^><^vv>v<^v<<v^v<<^<>^><^<>v^>v<v^>>^^v^v<^>^><>><^^v<<<vvv<<v^^>^v>><^vv<^v>>vv<^vv>><^><<<^^^<^>vvvv<^v>>^v>>v^>^vv<v<v>v><v<>^v<>^vvvv^v><>^v^^><^>v>v^><v^^^<^v><v^v<><<v>^<>^><v>>vv^<<v^v>^>>v<<^vvv<>>>v^v><><<<<v><v<>^^><<v^v<>^^v<vv>><>vv^<>v<vv<><^<^<<v^>v<>>>>^<^>>v>vv^<^<>^^<<>>vv<v<^>^<^>^^>>v^^>><<v^^^v>vv^^^v<>^v^>v^>>v>^^<^<<<^vvv<^vv^^^^v>>><v^v<^v>><<vvv><^^^<^v>><vv>v><vvvv^^<>>^^vvv>v^vv<^<>vvv>^^^>><^>v^<v<>^><>>v^>>^>>^>
^v^<^vv<^v^^^><v<^><^<v<><^^<v<>^>v<vv<vv>v^>vv^<^>^>>v^<<>><>^<<^v<v>^>v^vv^v<^v><^<v^^<v<><v>v<>>>^><vv<<^>^>^<^<>^v>v>>v>v>^^v^<<vv<^<v^>^^<^<<>^v^v^^vv<<<<^v>>vvv>^><v<^>>v<^^vv>^^<^<v<<><v^><^>v<<><v^v>^v^>^>^>v<><v>>>^^v<>>v<^<vv<vv>v^<v<>>v<<<^><^>v<vv<>^>><^v>^^v^>v^>v>>>><<><v^><^<><^<^^^<^^>>^^>^<v^><<v^v>v>>^v<>^^^^^v<v^v><>^^v<<v>>^<^v>^^<<^^<^><vv>>^>>>v^>><><v^<vv^^>vv^^>>v<vvv<^<^<><>^>v^v^<vv>^^<v<><vvv<v<^<v^v>^>><><^<^>^^^vv>><<^><><^v>v^v<^^vv>^^<^>>v<^><<^v^<<v^^^^>v<v<>^v^<^<v^>v<v>^>>vv^v^v^^><^<<>v>^^>v^^^<<^^vv^^^><^<v^<vv>v^<><<^^^^>><v<<<vv^<^vv<^^v^^^<>v^<^v>^v<v<^v<^>>^><>>v^<^v^><^v^v>>>v^^>vvv<<><><v><v^>^v>><v>^>>^v><^<^<<vv>^vvv><<>><^v>><vv^<><<v>v^<>v<<<<v^>^>><<<><>^<<^<vvv<>v^<<<<>><><>>^<v<^<>>^v^^v^v<^v>v^v^^<><>^v><<>^<v^<^vvv^v^^^v>v>v<<^^><<v<v<vvv><<^^<^^<v^<v>><^<v>>>v^^<><v>v^v<v^vvvvv>^v^<v^v>^^<v>>^^^><>v^^<^vv>^<^<>^<><>^>v^^><<<^>>v^>^v>v<>v<vv>><vvv<^^><<>v<<^vvv><>v<^v<<^vv^><<<<v><^v>^>v^vv^vvv><>><v>vv<^v^<<<^>><<^><>^><<>^<^>v><>v><^
<v>v<v^^><>^<v><vv^<^vv^^^<<<v><^>>>v^<>><<v<>^><>^>vv^>vvv>v><v^^><v<v><^^<^v<vv^><>^v>>v^>>^^^v^<vvv^>>v^^^><<^>>>^^>v^v^v^<<^^<<><><^^<^^^<<<vv<^^^<v^>vv^^<^^v>^><<<>vvv^^<v<vv<^^^^>v>v<vv>vvv^<>>^><<>^vv>>>^v>>v>^^>^><<vvvv<>^>^<v^v<v><^v^<v^vv^><^v<>v<><<>^<<^vv^vv<>>^^v^vv><>^<^>><><<^v<<^v>><v<v><>^><^vv<<^<vvv>^<v>^v^^vv<v>><><^>v>^><v><^<^<^>^<<>^<vv>v><v<<>>>vv>><^>>vvv<^<vvvv^<^<<>^v<v^<><<<>^<>>>v^v^v^><<v^^v^vvv<v<<^<<vvvv<^^>v>><^<>v>^>v<^^v<><v>^^^vv<^v^>>^^v<^<^v^^v<v>^v^^^<vv>^<<>^^vv>^^>v><^>><vv>>vvv<v<>v<>^>^<<><<^><>vv<>>>^vv>>>>v>^<v^v>>v>^<^<<<v<^^v>vvvvv^<v^v<^><>^>v>v^<^^^^^<vv>>v><>^v^<^v^v>^v^^<^<<^^<v>^v^^>^v<^v>^vvv<<vv^>^^v<v>vvvv^<>><<v>v^vv^<<<>vv^>^<v^^>^>v^<^<v<^^v^^^vv<><<<v>v<^<><>v<<>^<^>^><^v^^v>vvv^>^<vv^>vvv><><v>v>vv>>v><>><<<><^>vv^^^v<<^^<<v^><<v<>^>^<v><^^^v<>v<><<><<<v<<>>v^^<^<><vv<^^v<><><<><>>^^v^vv^v>^><^<<>v^<^^<><vv<^<><v^^<><<vvvvv<<v>^^^<v<<>v<>v<v<><>>^v<^<^v<<<>^v<<v><<<<<vv<^<v^<v><vv^^v<vvv<^v>^^^>^<^><^>^<^>>vv^<>v^>>^<^><>v>>v>
>v<<<^>^<<v>^<^^>>^<>>^>^<^<>^>^^^<><^>v<<vv>v>vvv<^><^v>vv>>^>^v^<^v>>^v^v<^>^<><^>^>><<v<vv>^<<>v>v<>v>v<vv<^<^><>>v^>v<<^<>>v><<<<^<v<^>>vvvvv>vvv>vv<<>>>>vv>vvv^<^v^v>v>v<<<<>^<v^^v>>^<><^^v><<>^^v^^v>v><vvvv^v<^>^v^^v>^<v<vv^<^>v><v<<v^^^v^v<v<>^vv^<^^^><v<^<<>^vv^v<v^^<v^>^>v<vv>>v>>v><<^^<v<v<^>v^^v^v^>>v^>^^^^<v<v<vv>v<v>vvv>>^v^vv<^>>v>><v^>v>vv<^>v^v^^><v<<v^v^v<>>v<<<v<^<<^<<v^>><^<vv<>v<>>><vvvvv^<<vv^<^<^><<v<>^^^>^>^<><<v<>^<<<>>v><>><^vv^><<^<>v>^v<>^^^v^<^<<vv<<<>^^>v><^^^><>>v^v>^>^>>^v^v>>^v<^^>^^>>><<^^>^v><<v><^<v<>>^vv<<<>v>vv^vvvv^^>><<v>>v>v<>>>>v<<vv<^^<^v<^^>v>^<vv><v>vv^^v<v<>v><v^>>^>^<^>>>>^^v<v<^>>>>v>^^>>^^>^>v><^>v^<^v<<v<^v<<vvv^^>^^><v>v^>>^>v><v^v<v>>^^^<^<>^>v^v<^^^^<v<<^<>v>>^<v^<<>v^^<<^<v^<>^>^<v^<v^^<>>v^<<^>v^>vv<^v^vv>^^vv>^v><>><<vv^^<>^v><<><v^v^v>^v<>^<^^^>>^^vv^vv>^v^vvv>v<^<<<>^><>v^v<>v<<><^v<<>>>v><>^>^^v^<^v><<^^^^><^>v<>^<v><>^<^<<^^><v<><><<>^vvv><<^^v>>v^^^v^^>v>^^><>^vv><^^<<<^^><<v>v^>^>^>^<>>><<v^^^><^v<<>^<^<^v><v^>>vv<<>v^>>>v<v>
v^^<>>>v<v^>^v><vv^<^^^<v^>^<vvvv^^^^vvv<v><^vvv<^^v^<<><>>><<^v^<><^^vv<>^<v^v><vv^<>vv<^<^^>v>>>v^v<>^<>^vv^vvv^>^<><v^v<^<<v<<v^^<^<vvv<vvvvv>^v>vv>^<vv>><v>^<<^^^>>><v^v>><<<>^>>v^^^v^^<v^vvv<><vvv>v><^v<vv><<<>><>>^<v><<^>^>>^><>v<v><>v<>>>>>>^<^<^vv<>v>^>^<<^<^^^^^^v><^v^^<v><<>^>v<v<<<^>^v^<<^<^<>^<>><vv<v^^v<<vv^^<v^^>>><<<<v^v>>v^><>^><^v>>><>^>>v^<^^^^>v^<v<><>>^>>v>^v>>^<v>>v>^^^<<<^^<>>>>^>vv>^v^^<<^<^<<><^>v>v^v<><>>^v^>^^^^^v^<vv><v^v^v<^<<>^^v^<v<vv>^>>v><>^><<>><><<vv^^<^<v<^^>>^^v<vvvvv^v>v^v>^v^v>><v>^>><^^><>>v<<<>><^vv^<<<^^^><>^><^>v>v>v^vv^>^^^vv^^><^^><><<^<<vv^^v>v>v>^><<<<^^v^^^v^>>vv<<<>vv>>>^v>v>><>v<v^<>^^>><<><v<<^^<^>vv<<<<>>^><<<>>^>>>>v<^v^>v><><>v^^^<<^^vv<>^vvvv><>v^v><<><v>^vv<vv<<>>^^>>v>><^<<vv^<>v^<^^>>v>>^^>v^^vv^<v>^<^^<><^><v<v>v<>^>>v<<<vvvv<^>v^vv>^v<vv>>v<vv^v><<v<^<><v><v^v><<^>^<v^>^v>vv><>><<>v>>v>>>><vv<v<>^^<v<^<<>^>^^<vv>>^vvv^vvv>^^<<>>^v^^<>>v>v^>^^^v>>v>^>^v<^>^<><<v>^<v<vv^<vv^v^<v>>^v>^><^v>v>>>v<><vv>v^<^>vv^><v^vv<v><v^v><<<vv^<v
<^>^<<v^<vv^^^^>v<>v<^>^^^v^><^><<v<v^v<vv><^v<>^<v^>v><>v><^<<><<v<^v^<v<><v^v>^<<>^>^<v<^^<^<>^^<v><>^^v^<v>><>^v><v^^vv<><v>^<v^^<><vv^>><>><<>>>vv<<^^^>^>^<><<^><>^<<>><^<^>vv><<<<^>^<<^<<v><^^v<^<<v>^v^<^<v<>v^v<vvvv^v^^v>v>><v<v>>v^>vvv>>>vvv^v^^<>><vv>>^<><>>v<^v^^v^<>^^v>>^^>><^>><v<><<<^v^>v><v>^v><vv<<<<v^v<<>v<<<><>>^>>^^<v<>v>>v>^>^^<<vv<<<^v>><^><^v><^>v^>^<>^^^vv<>vv>^vvvv<<><<v>>^v<vv^^<>v^>^<v><>v<v<^vv>vv^vv<^^<>v<><v<vvvv>><^>>^v>^<<>^>v>vv^>>^<^^v<^>v<<^^><<^^>>>>>^^^v<v^^<><^<>^v><<>^<<vv<<^^vvv<^<^<<vv^v<v<>^<v^v<<<<^^^vv<<><^<^^v<^vv>^<<v^<><>^vv^>^<<<>>vv^<<<v>^>>>^<<v<<<^v^><>^>^<v<>^^v<><v>>^^<<>v<v^v^v<>^>^><v>v>>><^^^<^v<>>^^^<><^vv^<^v><<<vvv<v><<v^>vvv<v>>^^^>><^^<><<^v^<^^<v<^<<^<>>>>^>>v^<<><<^v^v^v<vv<v<<<<v>^^>><^v>><^>>vv>^<v^<^v^^<><vv>v^v^^<<>>^>>^<^^^<^<^v>^<<^<vv<>v<><^v>v^>>vv^^><<<<vv<<v>v^><^<>vv<v><^<><v<><v>^^v<<^<>^><><>^vv^vv^^vv<^vv<>><^<v<^>>>v>>v<>^^>v^^>v^>^<>><v^^>v^^>vv<^<<^v<vv>>^vvv>><v^<^<<><v>>^v<<^v><<^v<>>>>^<<<<<^<<><<v>>v<^>><<
>^<<>vv<^<<>^v^^v<^^^<^>>^><vvv^^^v^<v><^><>>>><v<<v^vv^^^^^<^^vvv>v^^<^^><^^^vv>v^v<v<^v^v>^^^<><<^<<^v>>^v^^>v^v<v><<v^>>^^<^vv><v^v^<^<v>v><>^>^>vvv<>>^v>^v>><>^^v>^>^^vvv><<><v^<>vv><>^>><<<^<vv<v^v>>v>v<<>vv>><><v>v<>^<v>v^<><>v>vv>^v>v<vv<^>v<<>>^<^^>v^v><vv<<>>v><>>>>^><<<<v>>^^<<<^>v<v<<<><<<vv>^>^vv^<<^v>>v<v^vvv><vvv<^>^vv>>v^v^^v^^<<v>>^^^^^^>v<>^v<v^v>v<^^^>^<<>>vv<>v>v<<v^<>^<>^vvv>v^vv<>>^^>>>>^vv>^^>^v<^^>^>><^^>>^v><<^vv<v^v<v^vv^v<<><<^vv^^vv>^v>^^>>^v<><><<v^v><<>^<^>>vv<^<v<vv<>>^>>^>^v<v<<>^<v><>^<>^^^<>vv^<<>vv><<v^>^^vv^vv<<<^v^>>>v^v>^v^^v^>v<vv^^<v^^^<<<v^>>><^<v<v<^><^v^<>v><^^><^<>v>>vv<<>^>>^vvv^^>^<^v^<v>v<<>v^>>^<>>v>vv>>v>>>^<vv<vv>v^v>v<v>^v^>v^^^vvv<^<>v^<^>vv<>>vv<^^v>v^>^<^^^<<<v<<<<^^^^v^v^vvv>v^^vv<^>v<v^<^>>>>>v^^v><>v^<><>v^v^<^<>>^^<<<v<^v^>>>^^^<<^>><<<<vv>v^^^^>^>v^>^v<^<^<v<<v<vvv^><v>>>vv>^v<>v>><<v>>^^v>^v^<>v<v^v<<^v><vvv<v^v>>^^v^><^<v^^^^<>^v<v>v^v^^v<^^>v^^^v>v<<vv<^><v>vv<><>>^v^>v^vvv>>v^v^v>^<>^v>v><>^v^^<v<^>>><<>^>v>>^v>>^v<vvvv><<>v
><v<>^^>^vv>vv>>>><<^v^<v>^<^<v<^>>^>v^v<<>^^^<v>vv>>^><>>v<>^><<><<>v>^><^^<<^^><>v<vvv^>>^^>><^<^<>v^v^>><vv<<>><^<><<^v^>vv<v<<>vvv<^v><v<<<<>>v<<>v>v^<vv<vvv>v>><^vv>v<<><^vv><>><v>>vv^<vv^<<v>vvv<^^>^><<vv<^>>><^v<v<<^>^v<<><<v^>vvv<v>vvv<v<^^>>^v^><^^>v<>><<^><>v>><>^vv<>><<<v<^<vv>^<^<^<>><v^^v<^^^>>v<v><<v^v<v^vv^^v><v<v><><<>^v><vv^v>^^v<vvv<<<<^>><^vv<^v>><<v<<>v><>^<<>>>><<^<vv^v<v>><<>>>v^<vv<v<<<>v^v>^v^vv<v^v^^^<>>>v<^v^<<<<^v^<vv>>^<<<^^>>>^<v>^>>>>^^v<<><>>^<<<<<<><v<v^<^^vv>^^^v^>>v<v^^><<v<>^>^><v>>>^vv^^<>^^v><<v>^>^>^v<vv<<<>>>^^v<^^<<^<><<^>>^>vv>^>>^>v>>^^>>>>^^<>^<><<<<><>>v>v^<v^^^vv>>>>>v^^^<^^vv^v^>><>^^^^v><^<v<v^v<<v<^v<vv<>v^v<>>v<^v^v<v^<vvv><v>v^>v<<^^<<<v^<>^>>^^<<^>vvv<>vvvvv>v^><<<>>^>>^^>v^>^<^><><v<<^^<<v^<v>^<vv>><><<><>^<><^v>^><^><<v<<<<^^<<>>v^<<>v>^vv<v<^^^vvv<v<v<<<vvv><^>v>vv<<>>v>^<<<>v>v<<vv>v>^>vvvv>^><^^>>v^v<v>^<v>>^^v>^><v^^^v^>vv>^vv<<<v><v^<v^^>^v<<v<v^>^vv><^v^><^<>v^v<<<vv<<^v>>^^^<><<<v^<>>^^><>>vvvv^^<><v<<<>v^>^v<<>vvv^v>^<<^<v<>>"

#eval solvePart1 input
#eval solvePart2 input
