(* our first theorem *)
Theorem plus_O_n :
  forall n : nat,
    0 + n = n.
Proof.
  intros n.
  simpl.
  reflexivity.
Qed.


(* 
   When humans do pencil-paper proof we have a
1) Scratch pad with facts we know
2) Facts we want to show
Coq has the same implemented as
1) Context
2) Goal(s)
As the proof progresses the items in the scratch pad changes
e.g.
-learn new stuff
-transform the goal to show to something new/different we need to show
All this is expressed formally in
- Coqs/ITPs term language for expressing mathematical statements
- ITPs formal system (e.g. what strict rules of inference/deduction are legal)
 *)


Inductive nat': Type :=
  | O' : nat' (* Zero *)
  | S' : nat' -> nat'. (* Successor constructor *)

Compute O. (* 0, Zero *)
Compute S O. (* 0+1 = 1 *)
Compute S (S O). (* (0+1)+1 = 2 *)
Check S (S O).

Fixpoint plus (n : nat) (m : nat) : nat :=
  match n with
    | O => m
    | S n' => S (plus n' m)
  end.

Compute 2 + 1.
Compute plus (S (S O)) (S O).
(*  plus (S (S O)) (S O)
==> S (plus (S  O) (S (S O)))
      by the second clause of the match
==> S (plus (S O) (S O))
      by the second clause of the match
==> S (S (plus O  (S O) )
      by the second clause of the match
==> S (S (S O))
      by the first clause of the match
*)

(* 
   plus gets the successors constructors of the FIRST nat and puts them in front
   of the second nat
 *)

(* Induction Fail *)
Theorem plus_n_O_FailedAttempt : forall n:nat,
  n = n + 0.
Proof.
  intros n.
  simpl. (* Does nothing! *)
  (* intuitively, if you see the definition of plus, it tries to match
     the n (an opaque variable) to 2 construtors but it matches netheir,
     thus, it gets stuck since simpl. can't change the current goal
   *)
Abort.

(* 
   way to fix it is by (structural) induction on how the natural number could have
   been built.
*)

Theorem plus_n_O : forall n:nat, 
  n = n + 0.
Proof.
  intros n.
  induction n as [| n' IHn'].
  (* Base case: n = 0 *)
  -simpl. reflexivity.
  (* Inductive step: n = S n' = n' + 1 *)
  -simpl. (* uses definition of plus, puts the successor outside *)
   rewrite <- IHn'.
   reflexivity. 
Qed.