export Function (curry uncurry)

def dup (f : α -> α -> β) (x : α) := f x x

namespace Nat

  def addInt (lhs : Nat) : Int -> Nat
  | .ofNat rhs => lhs + rhs
  | .negSucc rhs => lhs - rhs.succ

  def maxInt (lhs : Nat) : Int -> Nat
  | .ofNat rhs => max lhs rhs
  | .negSucc _ => lhs

  def diff (lhs rhs : Nat) :=
    Int.ofNat lhs - Int.ofNat rhs

end Nat

namespace Std

  instance (i : Nat) (r : Range) : Decidable (i ∈ r) := by
    unfold Membership.mem
    unfold instMembershipNatRange
    infer_instance

  example : 0 ∈ [:1] := by decide
  example : 0 ∈ [0:1] := by decide
  example : 0 ∈ [0:1:1] := by decide
  example : 0 ∈ [:1:1] := by decide

end Std

namespace StreamRange

  structure StreamRange where
    start : Nat := 0
    step : Nat := 1

  instance : Membership Nat StreamRange where
    mem r i := if r.start + r.step >= r.start then r.start <= i else r.start >= i

  instance (i : Nat) (r : StreamRange) : Decidable (i ∈ r) := by
    unfold Membership.mem
    unfold instMembershipNatStreamRange
    infer_instance

  instance : ForIn m StreamRange Nat where
    forIn x b f := do
      let mut i := x.start
      let mut b := b
      while true do
        match (<- f i b) with
        | .yield b' => do
          b := b'
          i := i + x.step
        | .done b' => do
          b := b'
          break
        i := i + x.step
      return b

  syntax:max "[" withoutPosition(":") "]" : term
  syntax:max "[" withoutPosition(term ":") "]" : term
  syntax:max "[" withoutPosition(":" ":" term) "]" : term
  syntax:max "[" withoutPosition("::" term) "]" : term
  syntax:max "[" withoutPosition(term ":" ":" term) "]" : term
  syntax:max "[" withoutPosition(term "::" term) "]" : term

  macro_rules
  | `([:]) => `({ start := 0, step := 1 : StreamRange })
  | `([ $start :]) => `({ start := $start, step := 1 : StreamRange })
  | `([: : $step ]) => `({ start := 0, step := $step : StreamRange })
  | `([:: $step ]) => `({ start := 0, step := $step : StreamRange })
  | `([ $start : : $step ]) => `({ start := $start, step := $step : StreamRange })
  | `([ $start :: $step ]) => `({ start := $start, step := $step : StreamRange })

  example : 0 ∈ [:] := by decide
  example : 0 ∈ [::1] := by decide
  example : 0 ∈ [0:] := by decide
  example : 0 ∈ [0::1] := by decide

  instance : Stream StreamRange Nat where
    next? range := (range.start, { range with start := range.start + range.step })

  instance : ToStream StreamRange StreamRange where
    toStream range := range

end StreamRange
