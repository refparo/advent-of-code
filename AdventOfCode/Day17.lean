import AdventOfCode.Utils

namespace Day17

structure Machine where
  mk ::
  (A B C IP : Nat)
  out : Array Nat
deriving Inhabited

def parseInput (input : String) :=
  match input.toSubstring.splitOn "\n\n" with
  | [regs, program] =>
    let program := program.drop 9 |>.splitOn ","
      |>.map (α := Substring) (·.toNat?.get!)
    match regs.splitOn "\n"
      |>.map (α := Substring) (·.drop 12 |>.toNat?.get!)
    with
    | [A, B, C] => (program.toArray, Machine.mk A B C 0 #[])
    | _ => panic!"illegal input"
  | _ => panic!"illegal input"

def combo (mach : Machine) : Nat -> Nat
| 4 => mach.A
| 5 => mach.B
| 6 => mach.C
| lit => if lit < 4 then lit else panic!"illegal program"

partial def run (program : Array Nat) (mach : Machine) :=
  if h : mach.IP + 1 < program.size
  then run program $ step h
  else mach
where
  combo : Nat -> Nat
  | 4 => mach.A
  | 5 => mach.B
  | 6 => mach.C
  | lit => if lit < 4 then lit else panic!"illegal program"
  step (h : mach.IP + 1 < program.size) :=
    let operand := program[mach.IP + 1]
    match program[mach.IP] with
    | 0 => { mach with
      A := mach.A.shiftRight $ combo operand
      IP := mach.IP + 2
    }
    | 1 => { mach with
      B := mach.B.xor operand
      IP := mach.IP + 2
    }
    | 2 => { mach with
      B := combo operand % 8
      IP := mach.IP + 2
    }
    | 3 => { mach with
      IP := if mach.A == 0 then mach.IP + 2 else operand
    }
    | 4 => { mach with
      B := mach.B.xor mach.C
      IP := mach.IP + 2
    }
    | 5 => { mach with
      IP := mach.IP + 2
      out := mach.out.push $ combo operand % 8
    }
    | 6 => { mach with
      B := mach.A.shiftRight $ combo operand
      IP := mach.IP + 2
    }
    | 7 => { mach with
      C := mach.A.shiftRight $ combo operand
      IP := mach.IP + 2
    }
    | _ => panic!"illegal program"

def printOutput (mach : Machine) :=
  IO.println $ ",".intercalate $ mach.out.toList.map toString

def input := parseInput "\
Register A: 27334280
Register B: 0
Register C: 0

Program: 2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0"

#eval printOutput $ uncurry run input

/-
start:
B <- A % 8
B <- B ^ 2 = (A % 8) ^ 2
C <- A >> B = A >> ((A % 8) ^ 2)
A <- A >> 3
B <- B ^ 7 = (A % 8) ^ 5
B <- B ^ C = (A % 8) ^ (A >> ((A % 8) ^ 2)) ^ 5
out B % 8
if A != 0 then goto start
-/

def prevA (out : Nat) (nextA : Nat) :=
  let left := nextA.shiftLeft 3
  List.range 8 |>.filter (fun right =>
    (right.xor ((left + right).shiftRight $ right.xor 2)).xor 5 % 8 == out
  )
  |>.map (left + ·)

def findInitialA (out : Array Nat) :=
  out.foldr (init := [0]) (fun out prevAs => prevAs.flatMap (prevA out))
  |>.min?.get!

#eval findInitialA input.fst
