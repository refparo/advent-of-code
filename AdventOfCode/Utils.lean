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

section Prod

  instance [HAdd α1 β1 γ1] [HAdd α2 β2 γ2]
  : HAdd (α1 × α2) (β1 × β2) (γ1 × γ2) where
    hAdd := fun (a1, a2) (b1, b2) => (a1 + b1, a2 + b2)

  instance [HSub α1 β1 γ1] [HSub α2 β2 γ2]
  : HSub (α1 × α2) (β1 × β2) (γ1 × γ2) where
    hSub := fun (a1, a2) (b1, b2) => (a1 - b1, a2 - b2)

  instance [HMod α1 β1 γ1] [HMod α2 β2 γ2]
  : HMod (α1 × α2) (β1 × β2) (γ1 × γ2) where
    hMod := fun (a1, a2) (b1, b2) => (a1 % b1, a2 % b2)

  instance [HAdd α1 β γ1] [HAdd α2 β γ2]
  : HAdd (α1 × α2) β (γ1 × γ2) where
    hAdd := fun (a1, a2) b => (a1 + b, a2 + b)

  instance [HSub α1 β γ1] [HSub α2 β γ2]
  : HSub (α1 × α2) β (γ1 × γ2) where
    hSub := fun (a1, a2) b => (a1 - b, a2 - b)

  instance [HMul α1 β γ1] [HMul α2 β γ2]
  : HMul (α1 × α2) β (γ1 × γ2) where
    hMul := fun (a1, a2) b => (a1 * b, a2 * b)

  instance [HDiv α1 β γ1] [HDiv α2 β γ2]
  : HDiv (α1 × α2) β (γ1 × γ2) where
    hDiv := fun (a1, a2) b => (a1 / b, a2 / b)

  instance [Membership α1 γ1] [Membership α2 γ2]
  : Membership (α1 × α2) (γ1 × γ2) where
    mem | (xs, ys), (x, y) => x ∈ xs /\ y ∈ ys

  instance [Membership α1 γ1] [Membership α2 γ2]
    (pair : α1 × α2) (coll : γ1 × γ2)
    [Decidable (pair.fst ∈ coll.fst)]
    [Decidable (pair.snd ∈ coll.snd)]
  : Decidable (pair ∈ coll) := by
    simp only [Membership.mem]
    infer_instance

end Prod

namespace Nat

  def offset (a b : Nat) :=
    Offset.ofInt $ Int.ofNat a - Int.ofNat b

end Nat

export Nat (offset)

namespace Std

  instance : ToString Range where
    toString r := s!"[{r.start}:{r.stop}:{r.step}]"

  instance : Membership Nat Range where
    mem r i := r.start <= i && i < r.stop && (i - r.start) % r.step == 0

  instance (i : Nat) (r : Range) : Decidable (i ∈ r) := by
    simp only [Membership.mem]
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

  instance : HAdd Range Nat Range where
    hAdd r d := { r with start := r.start + d, stop := r.stop + d }

  instance : HAdd Range Offset Range where
    hAdd r d := { r with start := r.start + d, stop := r.stop + d }

  instance : HSub Range Nat Range where
    hSub r d := { r with start := r.start - d, stop := r.stop - d }

  instance : HSub Range Offset Range where
    hSub r d := { r with start := r.start - d, stop := r.stop - d }

end Std

namespace StreamRange

  structure StreamRange where
    start : Nat := 0
    step : Nat := 1
  deriving
    BEq, DecidableEq, Hashable, Inhabited,
    Nonempty, Repr, TypeName

  instance : Membership Nat StreamRange where
    mem r i := r.start <= i && (i - r.start) % r.step == 0

  instance (i : Nat) (r : StreamRange) : Decidable (i ∈ r) := by
    simp only [Membership.mem]
    infer_instance

  @[inline]
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

section Matrix

  structure Matrix (α) where
    array : Array α
    width : Nat
  deriving
    BEq, DecidableEq, Hashable, Inhabited, Nonempty, Repr

  instance [Inhabited α] [ToString α] : ToString (Matrix α) where
    toString mat := Id.run do
      let mut str := "["
      str := appendRow str (mat.array.toSubarray 0 mat.width)
      for start in [mat.width : mat.array.size : mat.width] do
        str := str ++ "\n "
        str := appendRow str (mat.array.toSubarray start (start + mat.width))
      str ++ "]"
    where appendRow (str : String) (row : Subarray α) := Id.run do
      let mut str := str
      str := str ++ toString row[0]!
      for elem in row.popFront do
        str := str ++ " " ++ toString elem
      str

  instance : GetElem (Matrix α) (Nat × Nat) α
    (fun mat (i, j) => i * mat.width + j < mat.array.size)
  where
    getElem
    | mat, (i, j), h => mat.array.get ⟨i * mat.width + j, h⟩

  instance : GetElem? (Matrix α) (Nat × Nat) α
    (fun mat (i, j) => i * mat.width + j < mat.array.size)
  where
    getElem?
    | mat, (i, j) => mat.array.get? (i * mat.width + j)
    getElem!
    | mat, (i, j) => mat.array.get! (i * mat.width + j)

  namespace Matrix
    def height (mat : Matrix α) := mat.array.size / mat.width

    def bounds (mat : Matrix α) := ([:mat.height], [:mat.width])

    def set! [Inhabited α] (mat : Matrix α) : Nat × Nat -> α -> Matrix α
    | (i, j), x => Matrix.mk (mat.array.set! (i * mat.width + j) x) mat.width

    def parseM! {m : Type -> Type l} [Monad m]
      (input : String) (f : (Nat × Nat) -> Char -> m α)
    := do
      let mut mat := Array.empty
      let mut width := Option.none
      let mut (i, j) := (0, 0)
      for c in input.toSubstring do
        match c with
        | '\n' =>
          match width with
          | .some j' => if j != j' then panic!"illegal input"
          | .none => width := .some j
          i := i + 1
          j := 0
        | c =>
          mat := mat.push (<- f (i, j) c)
          j := j + 1
      match width with
      | .some j' =>
        if j' != j then panic!"illegal input"
        else return Matrix.mk mat j'
      | .none =>
        return Matrix.mk mat mat.size

    def parse! (input : String) (f : (Nat × Nat) -> Char -> α) :=
      Id.run $ parseM! (m := Id) input f
  end Matrix

end Matrix

syntax num &"n" : term
syntax num &"i" : term
syntax num &"o" : term
syntax num &"u" : term
macro_rules
| `($n:num n) => `(($n : Nat))
| `($n:num i) => `(($n : Int))
| `($n:num o) => `(($n : Offset))
| `($n:num u) => `(($n : USize))
