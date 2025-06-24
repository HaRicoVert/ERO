## Donnees

octobre -> avril
3000 employes
2000 chasses neige
200000 tonnes de sel a placer sur le sol
10000 km de route
165M$ de budget

### Couts :

Drone:

- 100 euro / jour
- 0.01 euro / km

Vehicules de denneigement :

Type 1 :
- 500 euro / jour
- 1.1 euro / km
- 1.1 euro / h les 8 premieres heures
- 1.3 euro / h en dehors des 8 premieres heures
- vitesse moyenne : 10km/h

Type 2 :
- 800 euro / jour
- 1.3 euro / km
- 1.3 euro / h les 8 premieres heures
- 1.5 euro / h en dehors des 8 premieres heures
- vitesse moyenne : 20km/h

---

## Contraintes

-> respect du code de la route
-> les vehicules denneigent en un seul passage les routes a double sens
-> Potentiellement rajouter les conditions meterologiques si jamais on a du temps en plus mais pas demande dans le sujet

---

## Objectifs
-> Proposer differentes solutions qui optimisent differentes variables, couts, temps, avec ou sans machine type 2.

Chaque modele doit essayer de reduire les couts, le temps de trajet du drone et des chasse neige le plus possible.


## TODOS
-> Convertir les routes de Montreal en graph oriente pondere
    justification du graph oriente pondere :
        - certaines routes ne sont pas a double sens (oriente)
        - toutes les routes ne sont pas toutes autant enneige (pondere)

-> Definir les variables optimisables
voir ce cours du MIT pour comprendre : https://ocw.mit.edu/courses/6-251j-introduction-to-mathematical-programming-fall-2009/e191f18667dedc48774b5efc08a6d125_MIT6_251JF09_lec24.pdf

-> Poser le probleme mathematiquement sur feuille

-> Rentrer les variables et donnees sous forme de matrices en python

-> Creer un algorithme optimiser en terme de temps et couts pour le trajet du drone
    - il doit scanne tout montreal et donner des infos sur l'enneigement sur chacune des rues

-> Resoudre le ILP https://apmonitor.com/wiki/index.php/Main/IntegerProgramming

