<!--
.. title: Credit scoring
.. slug: credit-scoring
.. description: Réduire les risques liés aux prêts bancaires en prédisant la probabilité des défauts de de paiement.
.. date: 2026-01-01 00:00:01
-->

### Introduction

L’objectif n’était pas seulement d’obtenir de bonnes performances statistiques, mais de livrer un **système de décision fiable, explicable, industrialisé et monitoré**, capable de répondre aux enjeux du crédit à la consommation.

---

### Contexte et problématique métier

Le projet démarre dans un contexte de forte pression opérationnelle.
Chez *Prêt à Dépenser*, l’équipe **Credit Express** cherche à réduire au maximum le temps de décision pour l’octroi de crédit. En parallèle, la direction des risques est confrontée à une augmentation des impayés.

On se retrouve donc face à une tension classique :
**aller vite**, sans **augmenter le risque**.

Mon rôle a été de trouver un équilibre entre ces deux exigences, en tenant compte de contraintes fortes :

* des données déséquilibrées,
* des obligations de transparence et d’explicabilité,
* et un besoin de mise en production rapide.

Le besoin métier est alors clairement formulé : produire un score de probabilité de défaut, associé à une décision d’octroi, explicable et utilisable en production, avec un suivi dans le temps.

---

### État initial et diagnostic

Lorsque j’analyse l’existant, je constate qu’il n’y a pas encore de solution en production.
En revanche, il existe une base de travail solide : des notebooks de modélisation, des datasets riches issus de plusieurs sources, et un premier travail de feature engineering déjà aligné avec la logique métier.

Le problème n’est donc pas la qualité de l’exploration, mais le **passage à l’échelle**.

Plusieurs écarts majeurs apparaissent :

* pas d’API stable pour exposer le modèle,
* pas de contrat de données clair,
* pas de monitoring en production,
* et une traçabilité incomplète malgré l’usage de MLflow.

À ce stade, la solution est techniquement intéressante, mais **non exploitable par le métier**.

---

### Choix de la solution cible

La solution cible que je propose repose sur un principe simple :
**faire moins, mais mieux, et surtout durablement**.

Côté modélisation, je privilégie des modèles tabulaires robustes, bien adaptés aux données de crédit. Ils offrent un bon compromis entre performance, stabilité et explicabilité.
L’objectif n’est pas de maximiser un score abstrait, mais de maîtriser le coût métier, notamment en pénalisant fortement les faux négatifs.

L’explicabilité est intégrée dès la conception, à deux niveaux :

* globale, pour comprendre les facteurs de risque dominants,
* locale, pour justifier une décision sur un dossier précis.

Côté industrialisation, l’architecture s’articule autour de briques simples et open source :

* MLflow pour le suivi des expériences et des versions,
* une API FastAPI pour le scoring,
* Docker et CI/CD pour un déploiement reproductible,
* et un système de logs structuré alimentant le monitoring.

Le modèle devient ainsi un **service**, et non plus un simple fichier de sortie de notebook.

---

### Cas d’usage et valeur métier

Quatre cas d’usage principaux sont priorisés.

D’abord, le scoring standard, exposé via une API, utilisé directement dans le parcours d’octroi.
Ensuite, un scoring minimal, avec un nombre réduit de variables, pour des parcours rapides.
Troisièmement, l’explicabilité locale, essentielle pour les analystes crédit et la conformité.
Enfin, le monitoring continu, pour détecter les dérives de données ou de performance avant qu’elles n’impactent le métier.

Cette approche permet une adoption progressive par les équipes, tout en sécurisant la production.

---

### Démarche projet et pilotage

Sur le plan méthodologique, je m’appuie sur une démarche inspirée de CRISP-DM, mais exécutée de façon agile.

Le projet est découpé en phases courtes :

* cadrage métier et exploration des données,
* préparation et modélisation avec sélection d’un seuil métier,
* industrialisation et tests,
* mise en place du monitoring,
* puis optimisation et sécurisation des performances.

Les décisions sont systématiquement appuyées par des indicateurs clairs.
Côté business : taux d’acceptation, pertes nettes, délai de décision.
Côté machine learning : AUC, recall, score custom, calibration.
Côté opérations : latence, taux d’erreur, qualité des logs.

Ces KPI servent de langage commun entre le métier, la data et l’IT.

---

### Suivi, monitoring et maîtrise du risque

Un point clé du projet est le suivi post-déploiement.
Chaque prédiction génère des traces exploitables : distributions de scores, dérive des features, performance dans le temps.

Un tableau de bord permet de surveiller :

* le drift des données,
* la stabilité des scores,
* et les performances opérationnelles de l’API.

Un runbook est également défini pour guider les équipes en cas d’incident : identifier rapidement si le problème vient des données, du modèle ou de l’infrastructure.

On passe ainsi d’un modèle “boîte noire” à un **système maîtrisé et observable**.

---

### Conclusion et perspectives

Pour conclure, ce projet illustre le passage d’un besoin métier critique à une solution MLOps complète et exploitable.
Le modèle n’est pas seulement performant : il est **aligné avec les enjeux économiques**, explicable, industrialisé et surveillé dans le temps.

Les prochaines étapes sont clairement identifiées :

* mise en place de retrainings périodiques,
* amélioration éventuelle de la calibration des probabilités,
* enrichissement des dashboards avec des segments métier,
* et, à terme, une approche champion/challenger pour faire évoluer le scoring sans risque.