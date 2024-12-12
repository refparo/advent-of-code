import Std.Data.HashMap

namespace Day11

open Std (HashMap)

def parseInput (input : String) :=
  input.splitOn.map String.toNat!

def blink : Nat -> List Nat
| 0 => [1]
| x =>
  let s := Nat.toDigits 10 x
  if s.length % 2 == 0
  then
    let (l, r) := s.splitAt (s.length / 2)
    [l.asString.toNat!, r.asString.toNat!]
  else [x * 2024]

def solvePart1 (stones : List Nat) (n : Nat := 25) :=
  n.repeat (·.flatMap blink) stones

def blinkCounts (counts : HashMap Nat Nat) := Id.run do
  let mut result := HashMap.empty
  for (x, n) in counts do
    for y in blink x do
      result := result.alter y fun opt => .some $ n + opt.getD 0
  result

def solvePart2 (stones : List Nat) (n : Nat := 75) : HashMap Nat Nat :=
  n.repeat blinkCounts $ HashMap.ofList $ stones.map (Prod.mk · 1)

def input := parseInput "5688 62084 2 3248809 179 79 0 172169"

#eval solvePart1 input 25 |>.length
#eval solvePart2 input 75 |>.values.sum
