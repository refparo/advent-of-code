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

def blinkAll : List Nat -> List Nat
| []      => []
| x :: xs => blink x ++ blinkAll xs

def solvePart1 (stones : List Nat) (n : Nat := 25) :=
  n.repeat (·.flatMap blink) stones

def input := parseInput "5688 62084 2 3248809 179 79 0 172169"

#eval solvePart1 input 25 |>.length
