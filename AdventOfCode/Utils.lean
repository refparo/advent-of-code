export Function (curry uncurry)

def dup (f : α -> α -> β) (x : α) := f x x

section Offset

  @[unbox]
  structure Offset where
    ofInt ::
    toInt : Int
  deriving
    BEq, DecidableEq, Hashable, Inhabited,
    Nonempty, Ord, TypeName

  instance : Repr Offset where
    reprPrec a prec := reprPrec a.toInt prec

  instance : ToString Offset where
    toString a := toString a.toInt

  instance (n : Nat) : OfNat Offset n where
    ofNat := Offset.ofInt $ Int.ofNat n

  instance : Neg Offset where
    neg a := Offset.ofInt $ -a.toInt

  instance : HAdd Offset Offset Offset where
    hAdd a b := Offset.ofInt $ a.toInt + b.toInt

  instance : HSub Offset Offset Offset where
    hSub a b := Offset.ofInt $ a.toInt - b.toInt

  instance : HMul Offset Int Offset where
    hMul a b := Offset.ofInt $ a.toInt * b

  instance : HMul Offset Nat Offset where
    hMul a b := Offset.ofInt $ a.toInt * b

  instance : HDiv Offset Int Offset where
    hDiv a b := Offset.ofInt $ a.toInt / b

  instance : HDiv Offset Nat Offset where
    hDiv a b := Offset.ofInt $ a.toInt / b

  instance : HMod Offset Int Offset where
    hMod a b := Offset.ofInt $ a.toInt % b

  instance : HMod Offset Nat Offset where
    hMod a b := Offset.ofInt $ a.toInt % b

  instance : HAdd Nat Offset Nat where
    hAdd a b := match b.toInt with
      | .ofNat b => a + b
      | .negSucc b => a - b.succ

  instance : HSub Nat Offset Nat where
    hSub a b := match b.toInt with
      | .ofNat b => a - b
      | .negSucc b => a + b.succ

  instance : Max Offset where
    max a b := Offset.ofInt $ max a.toInt b.toInt

  instance : Min Offset where
    min a b := Offset.ofInt $ min a.toInt b.toInt

  namespace Offset

    def natAbs (a : Offset) := a.toInt.natAbs

    def maxNat (a : Nat) (b : Offset) :=
      match b.toInt with
      | .ofNat b => max a b
      | .negSucc _ => a

  end Offset

end Offset

namespace Nat

  def offset (a b : Nat) :=
    Offset.mk $ Int.ofNat a - Int.ofNat b

end Nat

export Nat (offset)

namespace Std

  instance : Membership Nat Range where
    mem r i := r.start <= i && i < r.stop && (i - r.start) % r.step == 0

  instance (i : Nat) (r : Range) : Decidable (i ∈ r) := by
    unfold Membership.mem
    unfold instMembershipNatRange_adventOfCode
    infer_instance

  example : 0 ∈ [:1] := by decide
  example : ¬ 1 ∈ [:1] := by decide

  example : 0 ∈ [0:1] := by decide
  example : ¬ 1 ∈ [0:1] := by decide

  example : 0 ∈ [:1:1] := by decide
  example : ¬ 1 ∈ [:1:1] := by decide

  example : 0 ∈ [0:1:1] := by decide
  example : ¬ 1 ∈ [0:1:1] := by decide

  example : 0 ∈ [0:3:2] := by decide
  example : ¬ 1 ∈ [0:3:2] := by decide
  example : 2 ∈ [0:3:2] := by decide
  example : ¬ 3 ∈ [0:3:2] := by decide

end Std

namespace StreamRange

  structure StreamRange where
    start : Nat := 0
    step : Nat := 1

  instance : Membership Nat StreamRange where
    mem r i := r.start <= i && (i - r.start) % r.step == 0

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
  example : 0 ∈ [0:] := by decide
  example : 0 ∈ [::1] := by decide
  example : 0 ∈ [0::1] := by decide

  example : 0 ∈ [0::2] := by decide
  example : ¬ 1 ∈ [0::2] := by decide

  instance : Stream StreamRange Nat where
    next? range := (range.start, { range with start := range.start + range.step })

  instance : ToStream StreamRange StreamRange where
    toStream range := range

end StreamRange
