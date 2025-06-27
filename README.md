# Déneigement de Montréal – Projet ERO

**EPITA, Apping1_C – Groupe 01**

## Auteurs

- **Rayann BOUHEDDOU**
- **Corentin DUPAIGNE**
- **Corentin GUINIOT-ALLOU**
- **Paul MONTAGNAC**
- **Esteban PAGIS**

---

## Sommaire

- [Introduction](#introduction)
- [Donnée et périmètre d’étude](#donnée-et-périmètre-détude)
    - [Collecte et préparation des données](#collecte-et-préparation-des-données)
    - [Optimisation des itinéraires](#optimisation-des-itinéraires)
    - [Coût et performance de déneigement](#coût-et-performance-de-dénéigement)
- [Hypothèses et choix de modélisation](#hypothèses-et-choix-de-modélisation)
    - [Hypothèses relatives à la mission drone](#hypothèses-relatives-à-la-mission-drone)
    - [Hypothèses relatives à la mission déneigeuse](#hypothèses-relatives-à-la-mission-dénéigeuse)
- [Choix de modélisation et comparaison des scénarios](#choix-de-modélisation-et-comparaison-des-scénarios)
    - [Solutions retenues et indicateurs de performance](#solutions-retenues-et-indicateurs-de-performance)
    - [Comparaison des scénarios](#comparaison-des-scénarios)
- [Les limites du modèle](#les-limites-du-modèle)
    - [Points positifs](#points-positifs)

---

## Introduction

Ce projet propose une approche algorithmique pour optimiser la gestion de l’enneigement à Montréal. Il repose sur la
modélisation de deux missions:

- une mission **de surveillance** par drone
- une mission **de déneigement** avec différents types de véhicules

Les deux missions sont représentées sous forme de graphes orientés, traités par le **problème du postier chinois
dirigé (DCPP)**. Le projet est implémenté en Python, avec des outils de cartographie tels que **OSMnx**, **NetworkX** et
**Matplotlib**.

---

## Donnée et périmètre d’étude

### Collecte et préparation des données

- Réseau routier de Montréal extrait via **OpenStreetMap** en mode **`drive`** (respect des sens de circulation)
- Niveaux de neige simulés entre 0 et 15 cm pour chaque tronçon
- Zone d’étude: 5 arrondissements de Montréal:
    - Outremont
    - Verdun
    - Anjou
    - Rivière-des-Prairies–Pointe-aux-Trembles
    - Plateau-Mont-Royal
- Les sous-graphes sont fusionnés et connectés via le graphe global de Montréal

### Optimisation des itinéraires

- Utilisation du **DCPP** : chaque tronçon est parcouru au moins une fois, avec le respect des contraintes
  directionnelles
- Graphe rendu par équilibrage des flux et ajout d’arcs
- Visualisation cartographique avec niveaux de neige colorisés via un colormap

### Coût et performance de déneigement

| Paramètre                               | Super Drone | Véhicule Type I | Véhicule Type II |
|-----------------------------------------|-------------|-----------------|------------------|
| Coût fixe (€/jour)                      | 100         | 500             | 800              |
| Coût kilométrique (€/km)                | 0.01        | 1.10            | 1.30             |
| Coût horaire (1<sup>ère</sup> 8h) (€/h) | –           | 1.10            | 1.30             |
| Coût horaire (>8h) (€/h)                | –           | 1.30            | 1.50             |
| Vitesse moyenne (km/h)                  | –           | 10              | 20               |

---

## Hypothèses et choix de modélisation

### Hypothèses relatives à la mission drone

- Autonomie **illimitée**, vol à altitude constante.
- Aucune modélisation des effets du vent, obstacles, trafic aérien ou erreurs GPS.
- Positionnement parfait et absence totale de contraintes réglementaires.
- Terre modélisée comme **plane localement**.

### Hypothèses relatives à la mission déneigeuse

- Pas de contrainte liée au carburant, à l’usure, au trafic ou à la météo.
- Déneigement supposé **constant** et indépendant de l’épaisseur de neige.
- Respect parfait des **restrictions OSM** (virages, sens uniques, etc.).
- Calculs réalisés dans un référentiel **localement plan**.

---

## Choix de modélisation et comparaison des scénarios

### Solutions retenues et indicateurs de performance

- Modélisation par **graphe orienté enrichi** de données de neige.
- Résolution via le **problème du postier chinois dirigé (DCPP)**.
- Indicateurs :
    - Distance totale
    - Temps estimé
    - Coût opérationnel (fixe + variable)

### Comparaison des scénarios

- **Déneigeuse Type II** : meilleure **rapidité**, mais **coût élevé**.
- **Déneigeuse Type I** : solution **économique**, mais **plus lente**.
- **Drone** : utile en **complément** pour la détection des zones critiques.

---

## Les limites du modèle

### Points positifs

- Modèle **reproductible** et **flexible**.
- Bonne **visualisation des résultats**.
- Intégration de **contraintes réalistes** tout en maintenant une complexité maîtrisée.
- Bonne séparation des missions de **surveillance** et de **déneigement**.

---

## Structure du projet

```
├── drone/
│   ├── main.py
│   └── utils.py
├── common/
│   └── utils.py
├── .env
└── README.md
```

---

## Dépendances

- `osmnx`
- `networkx`
- `matplotlib`
- `contextily`
- `dotenv`
- `python-dotenv`

```bash
pip install -r requirements.txt
```

---

## Lancement du projet

```bash
python3 drone/main.py
```

et

```bash
python3 snowplow/main.py
```