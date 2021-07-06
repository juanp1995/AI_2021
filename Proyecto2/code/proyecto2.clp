;(load "/home/juanp1995/Documentos/I-2021/Inteligencia_Artificial/Proyecto2/code/proyecto2.clp")

;####################################################
;TEMPLATES
;####################################################

(deftemplate indice-pregunta "Numero de pregunta"
    (slot pregunta (type SYMBOL) (allowed-symbols a b c d e f))
)

(deftemplate distancia "Plantilla distancia (semitonos)"
    (slot distancia-n (type INTEGER))
    (slot nombre (type STRING))
)

(deftemplate indice "Plantilla indice N(n)=k"
    (slot nota (type SYMBOL))
    (slot n (type INTEGER))
    (slot k (type INTEGER))
)

(deftemplate escala-existe "Plantilla para indicar si una escala existe"
    (slot exists (type SYMBOL) (allowed-symbols Si No Indef))
)


(deftemplate escala "Plantilla para una escala mayor"
    (multislot notas (type SYMBOL))
)


(deftemplate patron "Plantilla patron de escala mayor"
    (multislot pos (type INTEGER))
)


(deftemplate progresion "Plantilla de progresión"
    (multislot prog (type INTEGER))
    (multislot tone (type SYMBOL))
)


;####################################################
;HECHOS INICIALES
;####################################################

(deffacts notas "Notas musicales"
    (nota Do)
    (nota Do#)
    (nota Reb)
    (nota Re)
    (nota Re#)
    (nota Mib)
    (nota Mi)
    (nota Fa)
    (nota Fa#)
    (nota Solb)
    (nota Sol)
    (nota Sol#)
    (nota Lab)
    (nota La)
    (nota La#)
    (nota Sib)
    (nota Si)
)


(deffacts indice-k "Indice N(n)=k"
    (indice (nota Do) (n 1) (k -9))
    (indice (nota Do#) (n 2) (k -8))
    (indice (nota Reb) (n 2) (k -8))
    (indice (nota Re) (n 3) (k -7))
    (indice (nota Re#) (n 4) (k -6))
    (indice (nota Mib) (n 4) (k -6))
    (indice (nota Mi) (n 5) (k -5))
    (indice (nota Fa) (n 6) (k -4))
    (indice (nota Fa#) (n 7) (k -3))
    (indice (nota Solb) (n 7) (k -3))
    (indice (nota Sol) (n 8) (k -2))
    (indice (nota Sol#) (n 9) (k -1))
    (indice (nota Lab) (n 9) (k -1))
    (indice (nota La) (n 10) (k 0))
    (indice (nota La#) (n 11) (k 1))
    (indice (nota Sib) (n 11) (k 1))
    (indice (nota Si) (n 12) (k 2))
)

    
(deffacts distancias "Distancia entre notas (semitonos)"
    (distancia (distancia-n 0) (nombre "Unísono (perfecto)"))
    (distancia (distancia-n 1) (nombre "Segunda menor"))
    (distancia (distancia-n 2) (nombre "Segundo mayor"))
    (distancia (distancia-n 3) (nombre "Tercera menor"))
    (distancia (distancia-n 4) (nombre "Tercera mayor"))
    (distancia (distancia-n 5) (nombre "Cuarta (perfecta)"))
    (distancia (distancia-n 7) (nombre "Quinta (perfecta)"))
    (distancia (distancia-n 8) (nombre "Sexta menor"))
    (distancia (distancia-n 9) (nombre "Sexta mayor"))
    (distancia (distancia-n 10) (nombre "Séptima menor"))
    (distancia (distancia-n 11) (nombre "Séptima mayor"))
    (distancia (distancia-n 12) (nombre "Octava (perfecta)"))
)


(deffacts no-escalas "Escalas mayores inexistentes"
    (no-escala La#)
    (no-escala Fab)
)

(deffacts patron-escala "Patron de escala mayor"
    (patron (pos 2 2 1 2 2 2 1))
)


(deffacts patron-progresion "Patron de progresión"
    (progresion (prog 6 2 5 1) (tone m m M M))
)


;####################################################
;REGLAS
;####################################################

(defrule input-pregunta "Pregunta al usuario lo que desea consultar"
    =>
    (printout t tab "Ingrese la letra correspondiente a su consulta:" crlf)
    (printout t tab tab "a) Cálculo de frecuencia" crlf)
    (printout t tab tab "b) Intervalos simples entre notas" crlf)
    (printout t tab tab "c) Intervalo simple (inferior o superior) a partir de una nota" crlf)
    (printout t tab tab "d) Escala mayor" crlf)
    (printout t tab tab "e) Progresión circular de una escala mayor" crlf)
    (printout t tab tab "f) Salir" crlf)
    (assert (indice-pregunta (pregunta (read))))
)


(defrule salir "Sale del programa"
    (indice-pregunta (pregunta f))
    =>
    (exit)
)

;----------------------------------------------------
;FRECUENCIA
;----------------------------------------------------

(defrule input-frecuencia "Pregunta al usuario por la nota"
    (indice-pregunta (pregunta a))
    =>
    (printout t tab "Ingrese la nota músical:" crlf)
    (assert (notaCalc (read)))
    (printout t tab "Ingrese el subíndice de la nota músical:" crlf)
    (assert (sub-notaCalc (read)))
    (assert (notaCalc-k 0))
)

(defrule check-subIdx "Comprueba el subíndice"
    (indice-pregunta (pregunta a))
    ?note <- (notaCalc ?nota)
    ?subIdx <- (sub-notaCalc ?sub-idx)
    (test (or (< ?sub-idx 0) (> ?sub-idx 8)))
    =>
    (printout t tab tab "La nota " ?nota "-" ?sub-idx " no existe" crlf)
    (retract ?note ?sub-idx)
)

(defrule frecuencia "Calcula la frecuencia de una nota"
    (indice-pregunta (pregunta a))
    ?note <- (notaCalc ?nota)
    ?subIdx <- (sub-notaCalc ?sub-idx)
    ?notaK <- (notaCalc-k ?notaCalc-k)
    (test (and (>= ?sub-idx 0) (<= ?sub-idx 8)))
    =>
    (do-for-fact((?indiceK indice)) (eq ?indiceK:nota ?nota)
        (bind ?notaK ?indiceK:k)
    )
    (assert (frecuencia (* (* 55 (** 2 (- ?sub-idx 1))) (** (** 2 (/ 1 12)) ?notaK))))
)

(defrule frecuencua-respuesta "Muestra la respuesta del calculo de frecuencia"
    (indice-pregunta (pregunta a))
    ?note <- (notaCalc ?nota)
    ?subIdx <- (sub-notaCalc ?sub-idx)
    ?notaK <- (notaCalc-k ?notaCalc-k)
    ?frec <- (frecuencia ?frecuencia)
    =>
    (printout t tab tab "La frecuencia de la nota " ?nota "-" ?sub-idx " es: " ?frecuencia "Hz" crlf)
    ;(retract ?note ?subIdx ?notaK ?frec)
)

;----------------------------------------------------
;INTERVALO SIMPLE
;----------------------------------------------------

(defrule input-intervalo-simple "Pregunta al usuario por las dos notas del intervalo"
    (indice-pregunta (pregunta b))
    =>
    (printout t tab "Ingrese la primera nota:" crlf)
    (assert (nota1 (read)))
    (printout t tab "Ingrese el subíndice de la primera nota:" crlf)
    (assert (sub-idx1 (read)))
    (printout t tab "Ingrese la segunda nota:" crlf)
    (assert (nota2 (read)))
    (printout t tab "Ingrese el subíndice de la segunda nota:" crlf)
    (assert (sub-idx2 (read)))
    (assert (n 0)) ;Contador temporal
)


(defrule get-k "Obtener valor de k de dos notas"
    (indice (nota ?nota1) (k ?k1)) 
    (indice (nota ?nota2) (k ?k2)) 
    (nota1 ?nota1)
    (nota2 ?nota2)
    =>
    (assert (k1 ?k1))
    (assert (k2 ?k2))
)


(defrule get-frecs "Obtener frecuencias de las dos notas"
    (k1 ?k1)
    (k2 ?k2)
    (sub-idx1 ?sub-idx1)
    (sub-idx2 ?sub-idx2)
    =>
    (assert (frec1 (* (* 55 (** 2 (- ?sub-idx1 1))) (** (** 2 (/ 1 12)) ?k1 ))))
    (assert (frec2 (* (* 55 (** 2 (- ?sub-idx2 1))) (** (** 2 (/ 1 12)) ?k2 ))))
)


(defrule intervalo-simple1 "Intervalo entre dos notas 1 (nota1 > nota2)"
    (nota1 ?nota1) (sub-idx1 ?sub-idx1)
    (nota2 ?nota2) (sub-idx2 ?sub-idx2)
    (frec1 ?frec1) (frec2 ?frec2)
    ?tmp <- (n ?n)
    (test (>= ?frec1 ?frec2))
    =>
    (while  (> (- ?frec1 ?frec2) 0.001)
        (bind  ?frec2 (* ?frec2 (** 2 (/ 1 12))))
        (bind ?n (+ ?n 1))
    )
    (assert (semitonos ?n))
    (retract ?tmp)
)


(defrule intervalo-simple2 "Intervalo entre dos notas 2 (nota2 > nota1)"
    (nota1 ?nota1) (sub-idx1 ?sub-idx1)
    (nota2 ?nota2) (sub-idx2 ?sub-idx2)
    (frec1 ?frec1) (frec2 ?frec2)
    ?tmp <- (n ?n)
    (test (< ?frec1 ?frec2))
    =>
    (while (> (- ?frec2 ?frec1) 0.001)
        (bind  ?frec1 (* ?frec1 (** 2 (/ 1 12))))
        ;(printout t ?frec1 crlf)
        (bind ?n (+ ?n 1))
    )
    (assert (semitonos ?n))
    (retract ?tmp)
)

(defrule intervalo-simple-respuesta1 "Obtiene la respuesta del intervalo simple" 
    (distancia (distancia-n ?n) (nombre ?name))
    ?sm <- (semitonos ?n)
    ?n1 <- (nota1 ?nota1)
    ?n2 <- (nota2 ?nota2)
    ?s1 <- (sub-idx1 ?sub1)
    ?s2 <- (sub-idx2 ?sub2)
    ?tmp1 <- (k1 ?k1)
    ?tmp2 <- (k2 ?k2)
    ?f1 <- (frec1 ?frec1)
    ?f2 <- (frec2 ?frec2)
    =>
    (retract ?n1 ?n2 ?s1 ?s2 ?sm ?tmp1 ?tmp2 ?f1 ?f2)
    (printout t tab tab "Las notas " ?nota1 "-" ?sub1 " y " ?nota2 "-" ?sub2 
        " están a un intervalo de " ?n " semitonos, " ?name crlf)    
)


(defrule intervalo-simple-respuesta2 "Obtiene la respuesta del intervalo simple (compuesto)" 
    ?sm <- (semitonos ?n)
    ?n1 <- (nota1 ?nota1)
    ?n2 <- (nota2 ?nota2)
    ?s1 <- (sub-idx1 ?sub1)
    ?s2 <- (sub-idx2 ?sub2)
    ?tmp1 <- (k1 ?k1)
    ?tmp2 <- (k2 ?k2)
    ?f1 <- (frec1 ?frec1)
    ?f2 <- (frec2 ?frec2)
    =>
    (retract ?n1 ?n2 ?s1 ?s2 ?sm ?tmp1 ?tmp2 ?f1 ?f2)
    (printout t tab tab "Las notas " ?nota1 "-" ?sub1 " y " ?nota2 "-" ?sub2 
        " están a un intervalo de " ?n " semitonos, intervalo compuesto" crlf)
)


;----------------------------------------------------
;NOTA A PARTIR DE UN INTERVALO SIMPLE
;----------------------------------------------------

(defrule input-nota-intervalo "Pregunta al usuario por la nota y el intervalo"
    (indice-pregunta (pregunta c))
    =>
    (printout t tab "Ingrese la nota:" crlf)
    (assert (optC-nota (read)))
    (printout t tab "Ingrese el subindice de la nota:" crlf)
    (assert (optC-subIdx (read)))
    (printout t tab "Ingrese dirección del intervalo (superior/inferior):" crlf)
    (assert (optC-dir (read)))
    (printout t tab "Ingrese intervalo en semitonos (1,2...8,etc):" crlf)
    (assert (optC-semitonos (read)))
)


(defrule intervalo-superior "Determina la nota en intervalo superior"
    (indice-pregunta (pregunta c))
    (optC-nota ?nota)
    (optC-subIdx ?subIdx)
    (optC-dir superior)
    (optC-semitonos ?semitonos)
    (indice (nota ?nota) (n ?n))
    =>
    (bind ?tmp (+ ?n ?semitonos))
    (if (> ?tmp 12)
        then
            (bind ?tmp (- ?tmp 12))
            (assert (optC-newSubIdx (+ ?subIdx 1)))
        else
            (assert (optC-newSubIdx ?subIdx))
    )
    (assert (optC-N ?tmp))
)


(defrule intervalo-inferior "Determina la nota en intervalo inferior"
    (indice-pregunta (pregunta c))
    (optC-nota ?nota)
    (optC-subIdx ?subIdx)
    (optC-dir inferior)
    (optC-semitonos ?semitonos)
    (indice (nota ?nota) (n ?n))
    =>
    (bind ?tmp (- ?n ?semitonos))
    (if (< ?tmp 1)
        then
            (bind ?tmp (+ ?tmp 12))
            (assert (optC-newSubIdx (- ?subIdx 1)))
        else
            (assert (optC-newSubIdx ?subIdx))
    )
    (assert (optC-N ?tmp))
)


(defrule nota-intervalo-respuesta1 "Obtiene la respuesta de intervalo compuesto"
    (indice-pregunta (pregunta c))
    ?addr-nota <- (optC-nota ?nota)
    ?addr-subIdx <- (optC-subIdx ?subIdx)
    ?addr-dir <- (optC-dir ?dir)
    ?addr-semitonos <- (optC-semitonos ?semitonos)
    ?addr-newSubIdx <- (optC-newSubIdx ?newSubIdx)
    (test (> ?semitonos 12))
    (test (and (>= ?newSubIdx 0) (<= ?newSubIdx 8)))
    =>
    ;(retract ?addr-nota ?addr-subIdx ?addr-dir ?addr-semitonos ?addr-newSubIdx)
    (printout t tab tab "El intervalo indicado es compuesto" crlf)
)

(defrule nota-intervalo-respuesta2 "Obtiene el nombre de la nota al intervalo dado"
    (indice-pregunta (pregunta c))
    ?addr-nota <- (optC-nota ?nota)
    ?addr-subIdx <- (optC-subIdx ?subIdx)
    ?addr-dir <- (optC-dir ?dir)
    ?addr-semitonos <- (optC-semitonos ?semitonos)
    ?addr-newSubIdx <- (optC-newSubIdx ?newSubIdx)
    ?addr-N <- (optC-N ?N)
    (indice (nota ?nota-respuesta) (n ?N))
    (distancia (distancia-n ?semitonos) (nombre ?nombre))
    (test (<= ?semitonos 12))
    (test (and (>= ?newSubIdx 0) (<= ?newSubIdx 8)))
    =>
    (printout t tab tab "A un intervalo " ?dir " de " ?semitonos " semitonos (" ?nombre ") de " 
        ?nota "-" ?subIdx " se encuentra la nota " ?nota-respuesta "-" ?newSubIdx crlf)
    ;(retract ?addr-nota ?addr-subIdx ?addr-dir ?addr-semitonos ?addr-newSubIdx ?addr-N)
)


(defrule nota-intervalo-respuesta3 "Respuesta en caso de que nota no exista"
    (indice-pregunta (pregunta c))
    ?addr-nota <- (optC-nota ?nota)
    ?addr-subIdx <- (optC-subIdx ?subIdx)
    ?addr-dir <- (optC-dir ?dir)
    ?addr-semitonos <- (optC-semitonos ?semitonos)
    ?addr-newSubIdx <- (optC-newSubIdx ?newSubIdx)
    ?addr-N <- (optC-N ?N)
    (test (or (< ?newSubIdx 0) (> ?newSubIdx 8)))
    =>
    (printout t tab tab "A un intervalor " ?dir " de " ?semitonos " semitonos de " ?nota "-" ?subIdx 
        " no existe ninguna nota musical" crlf)
    ;(retract ?addr-nota ?addr-subIdx ?addr-dir ?addr-semitonos ?addr-newSubIdx ?addr-N)
)

;----------------------------------------------------
;ESCALAS MAYORES
;----------------------------------------------------

(defrule input-escala-mayor "Pregunta al usuario la escala mayor"
    (indice-pregunta (pregunta d))
    =>
    (printout t tab "Ingrese la nota de la escala: " crlf)
    (assert (nota-escala (read)))
    (assert (escala-existe (exists Indef)))
)


(defrule escala-no-existe "Indica que la escala no existe"
    (or 
        (and ?nt <- (nota-escala ?nota) (no-escala ?nota))
        (and ?nt <- (optE-nota ?nota) (no-escala ?nota))
    )
    ?ex <- (escala-existe (exists Indef))
    =>
    (retract ?nt)
    (modify ?ex (exists No))
    (printout t tab "La escala " ?nota " no existe" crlf)
)

(defrule escala-si-existe "Indica que la escala si existe"
    (or 
        (not (and (nota-escala ?nota) (no-escala ?nota)))
        (not (and (optE-nota ?nota) (no-escala ?nota)))
    )
    ?ex <- (escala-existe (exists Indef))
    =>
    (modify ?ex (exists Si))
)


(defrule escala-mayor "Determina las notas que forman la escala"
    ;(nota ?nota)
    ;(nota-escala ?nota)
    (or
        (and (nota ?nota) (nota-escala ?nota))
        (and (nota ?nota) (optE-nota ?nota))
    )
    (indice (nota ?nota) (n ?n))
    (escala-existe (exists Si))
    =>
    (bind ?notaN (+ ?n 2))
    (bind ?cnt 0)

    (bind ?escala (create$ ?nota)) ;Almacena las notas de la escala
    (if (> ?notaN 12)
        then
            (bind ?notaN (- ?notaN 12))
    )
    
    (loop-for-count (?cnt 2 7) do
        (do-for-fact((?pa patron)) (= (nth$ 1 ?pa:pos) 2)
            (bind ?patron-pos (nth$ ?cnt ?pa:pos))
        )
        
        (do-for-fact((?ind indice)) (= ?ind:n ?notaN)
            (bind ?notaAct ?ind:nota)
            (bind ?escala (insert$ ?escala ?cnt ?ind:nota))
        )
        
        (if (and (eq ?nota Do) (eq ?notaAct Mi))
            then
                (bind ?notaN (+ ?notaN 1))                
            else
                (bind ?notaN (+ ?notaN ?patron-pos))
        )
        
        (if (> ?notaN 12)
            then
                (bind ?notaN (- ?notaN 12))
        )
    )
    (assert (escala (notas ?escala)))
)


(defrule escala-respuesta "Muestra las notas de una escala"
    (indice-pregunta (pregunta d))
    (nota-escala ?nota)
    (escala (notas $?notas))
    =>
    (printout t tab "La escala de " ?nota " es: " ?notas crlf)
)


;----------------------------------------------------
;PROGRESIÓN
;
;Utiliza las reglas "escala-no-existe"
;                   "escala-si-existe"
;                   "escala-mayor"
;----------------------------------------------------

(defrule input-progresion "Pregunta al usuario la nota de la escala"
    (indice-pregunta (pregunta e))
    =>
    (printout t tab "Ingrese la nota de la escala: " crlf)
    (assert (optE-nota (read)))
    (assert (escala-existe (exists Indef)))
)


(defrule progresion "Genera la progresión vi-ii-V-I"
    (indice-pregunta (pregunta e))
    (optE-nota ?nota)
    (escala (notas $?notas))
    =>
    (bind ?n 0)
    (bind ?progresion (create$))
    (loop-for-count (?cnt 1 4) do
        (do-for-fact((?p progresion)) (= (length$ ?p:prog) 4)
            (bind ?pos (nth$ ?cnt ?p:prog))
            (bind ?tn (nth$ ?cnt ?p:tone))
        )

        (do-for-fact((?es escala)) (= (length$ ?es:notas) 7)
            (if (eq ?tn m)
                then
                    (bind ?progresion (insert$ ?progresion ?cnt (sym-cat (nth$ ?pos ?es:notas) -m)))
                
                else
                    (bind ?progresion (insert$ ?progresion ?cnt (nth$ ?pos ?es:notas)))
            )
        )
    )
    (printout t tab "La progresión de " ?nota " es: " ?progresion crlf)
)




