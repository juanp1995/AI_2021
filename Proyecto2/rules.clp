(defrule duck
    (animal-is duck)
    =>
    (assert (sound-is quack))
    (printout t "it's a duck" crlf))
    
(defrule is-it-a-duck
    (animal-has webbed-feet)
    (animal-has feathers)
    =>
    (assert (animal-is duck)))
