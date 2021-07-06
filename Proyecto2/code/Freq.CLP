(deftemplate K "la k de la notas"
(slot nota)
(slot k)
)

(defrule getk (frecuencia ?d ?i) (K (nota ?d) (k ?k)) => (printout t "K es" ?k crlf) (assert (getfrec ?d ?i ?k)))

(defrule frecuencia ?f<-(getfrec ?x ?i ?k) => (retract ?f) (assert (freq ?x ?i (* (* 55 (** 2 (- ?i 1))) (** (** 2 (/ 1 12)) ?k)))))

(deffacts initial 
(K (nota Do) (k -9))
(K (nota Do#/Reb) (k -8))
(K (nota Re) (k -7))
(K (nota Re#/Mib) (k -6))
(K (nota Mi) (k -5))
(K (nota Fa) (k -4))
(K (nota Fa#/Solb) (k -3))
(K (nota Sol) (k -2))
(K (nota Sol#/Lab) (k -1))
(K (nota La) (k 0))
(K (nota La#/Sib) (k 1))
(K (nota Si) (k 2))
)