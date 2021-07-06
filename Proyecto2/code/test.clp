(deftemplate escala "Plantilla escalas"
    (multislot notas (type SYMBOL))
)




(defrule runMyTest
    =>
    (printout t tab "Run test?: Si/No" crlf)
    (assert (runTest (read)))
)

(defrule myTest
    (runTest Si)
    =>
    (printout t tab "FIRE!!!!" crlf)
    (bind ?tmp (create$ Do))

    (bind ?tmp (insert$ ?tmp 2 Re))

    (printout t tab tab ?tmp crlf)
    (assert (escala (notas ?tmp)))
)