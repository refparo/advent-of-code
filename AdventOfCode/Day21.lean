import Std.Data.HashMap

import AdventOfCode.Utils

namespace Day21

open Std (HashMap)

class Keypad (α : Type) where
  keys : List α
  activate : α
  gap : Int × Int
  pos : α -> Int × Int

inductive NumKey where
| num (_ : Fin 10)
| activate
deriving BEq, Hashable, Inhabited

instance : Repr NumKey where
  reprPrec
  | .activate, _=> "A"
  | .num n, _ => toString n

instance : Keypad NumKey where
  keys := .activate :: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map .num
  activate := .activate
  gap := (0, 3)
  pos
  | .activate => (2, 3)
  | .num 0 => (1, 3)
  | .num n =>
    let n := Int.ofNat (n.val - 1)
    (n % 3, 2 - n / 3)

inductive DirKey where
| left | right | up | down | activate
deriving BEq, Hashable, Inhabited

instance : Repr DirKey where
  reprPrec
  | .left, _ => "<"
  | .right, _ => ">"
  | .up, _ => "^"
  | .down, _ => "v"
  | .activate, _ => "A"

instance : Keypad DirKey where
  keys := [.activate, .left, .right, .up, .down]
  activate := .activate
  gap := (0, 0)
  pos
  | .left => (0, 1)
  | .right => (2, 1)
  | .up => (1, 0)
  | .down => (1, 1)
  | .activate => (2, 0)

def parseInput (input : String) :=
  input.splitOn "\n" |>.map fun line =>
    line.toList.map fun
    | 'A' => NumKey.activate
    | c => let n := c.toNat - '0'.toNat
      if h : n < 10
      then NumKey.num ⟨n, h⟩
      else panic!"illegal input"

def costMatrix [k : Keypad α] [BEq α] [Hashable α]
  (cost : DirKey × DirKey -> Nat := fun _ => 0)
:=
  k.keys.foldl (init := HashMap.empty) fun mat a =>
    k.keys.foldl (init := mat) fun mat b => mat.insert (a, b) $
      if a == b then 0 else
      let (xg, yg) := k.gap
      let (xa, ya) := k.pos a
      let (xb, yb) := k.pos b
      let (dx, dy) := k.pos b - k.pos a -- -1, 0
      let xDir :=
        if dx > 0 then .right else if dx < 0 then .left else .activate
      let yDir :=
        if dy > 0 then .down else if dy < 0 then .up else .activate
      let costXY :=
        cost (.activate, xDir) + -- move in x axis, or don't move
        dx.natAbs + -- push |dx| times
        cost (xDir, yDir) + -- move in y axis, or return to activate
        dy.natAbs + -- push |dy| times
        cost (yDir, .activate) -- return to activate
      let costYX :=
        cost (.activate, yDir) + -- move in y axis, or don't move
        dy.natAbs + -- push |dy| times
        cost (yDir, xDir) + -- move in x axis, or return to activate
        dx.natAbs + -- push |dx| times
        cost (xDir, .activate) -- return to activate
      if yg == ya && dx.tdiv (xg - xa) > 0 ||
        xg == xb && (-dy).tdiv (yg - yb) > 0
      then costYX -- gap is on the XY route
      else if xg == xa && dy.tdiv (yg - ya) > 0 ||
        yg == ya && (-dx).tdiv (xg - xb) > 0
      then costXY -- gap is on the YX route
      else min costXY costYX

def cost (indirection : Nat) (prev : DirKey × DirKey -> Nat := fun _ => 0) :=
  match indirection with
  | .zero => costMatrix (α := NumKey) prev
  | .succ n => cost n (costMatrix prev).get!

def complexity (cost : HashMap (NumKey × NumKey) Nat) (code : List NumKey) :=
  let len := List.sum $
    (.activate :: code).zipWith (ys := code)
    (curry $ (· + 1) ∘ cost.get!)
  let numCode := code.foldl (init := 0) fun acc => fun
    | .num n => acc * 10 + n.val
    | .activate => acc
  len * numCode

def input := parseInput "\
319A
985A
340A
489A
964A"

#eval input.map (complexity $ cost 2) |>.sum
#eval input.map (complexity $ cost 25) |>.sum
