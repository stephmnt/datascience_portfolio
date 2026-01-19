<!--
.. title: Attrition ESN
.. slug: attrition-esn
.. description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
.. date: 2025-11-01 00:00:01
-->

## 1. Contexte et analyse des besoins

### 1.1 Présentation (organisation et / ou contexte)

Quand j'ai pris le projet en main, le constat était simple : la DRH disposait de trois exports de données (SIRH, évaluations, sondage interne) mais pas d'un outil fiable pour anticiper les départs. L'enjeu n'était pas seulement de produire un score, mais de créer un cadre de décision clair et traçable pour accompagner les managers.

Le contexte technique était favorable : une stack Python déjà choisie, la possibilité d'utiliser PostgreSQL, et un besoin de démonstration rapide (soutenance, déploiement léger sur Hugging Face). La maturité data est intermédiaire : données structurées et riches, mais pipeline et supervision encore à bâtir.

### 1.2 Collecte et analyse du besoin métier

Je me suis d'abord aligné avec les parties prenantes clés : RH (utilisateurs finaux), managers (bénéficiaires des alertes), data/IT (industrialisation), et conformité (RGPD, biais).

Le recueil s'est fait à partir des livrables existants du projet et de l'analyse du dépôt :

- compréhension des données brutes (3 fichiers CSV) et de leur usage ;
- analyse de la documentation et des choix techniques ;
- revue des modules clés (`main.py`, `app.py`, `projet_05/dataset.py`).

Les besoins ont été hiérarchisés autour de trois priorités :

1. fiabiliser la fusion des sources et la préparation des données ;
2. fournir un score de risque compréhensible avec un seuil de décision ajustable ;
3. garantir la traçabilité des prédictions (journalisation).

Contraintes majeures :

- disponibilité d'une base PostgreSQL en local, mais non sur Hugging Face (nécessité d'un fallback pandas) ;
- exigences de confidentialité et d'audit (journalisation des décisions) ;
- temps et budget limités pour une démonstration fonctionnelle.

## 2. Audit de la solution data existante (ou proposée si absence de solution existante)

### 2.1 Solution actuelle ou proposée

L'absence de solution existante a conduit à proposer une architecture pragmatique, modulaire et orientée démonstration :

- ingestion des trois sources via `scripts/init_db.py` vers PostgreSQL ;
- préparation et fusion dans `projet_05/dataset.py` ;
- feature engineering + entraînement via `projet_05/features.py` et `projet_05/modeling/train.py` ;
- modèle sérialisé dans `models/best_model.joblib` ;
- interface Gradio dans `app.py` avec onglets Formulaire, Tableau, CSV et données brutes ;
- journalisation des prédictions dans `prediction_logs`.

Flux simplifié :

```
CSV bruts -> PostgreSQL -> preparation/merge -> features -> entrainement -> modele
                                 |                                     |
                                 +-----------------> Gradio <----------+
                                                  logs predictions
```

### 2.2 Évaluation de l'adéquation aux besoins

Critères d'analyse :

- performance : inference rapide sur données tabulaires, pipeline de training séparé ;
- scalabilité : suffisante pour un POC, limite pour des volumes massifs ;
- coût : stack open source, déploiement léger ;
- pertinence métier : score explicite, seuil ajustable, logs d'audit.

Écarts et limites identifiés :

- dépendance à PostgreSQL pour le suivi fin ; sur Hugging Face, la journalisation est limitée ;
- couverture de tests partielle (zones non couvertes en modeling et explainability) ;
- absence d'un module d'explicabilité pleinement exploité dans la démonstration.

## 3. Identification d'une solution technique cible

Comparatif d'approches techniques :

- règles métiers simples : rapide, mais faible précision et faible adaptabilité ;
- ML classique sur données tabulaires (scikit-learn) : meilleur compromis qualité/complexité ;
- architectures plus lourdes (deep learning, MLOps avancé) : surdimensionnées pour le besoin actuel.

La solution cible retient un ML classique avec une couche de pilotage légère :

- PostgreSQL pour l'intégrité et la traçabilité ;
- pipeline Python orchestré par `main.py` ;
- interface Gradio pour un usage immédiat ;
- CI/CD GitHub Actions pour la reproductibilité.

Facteurs clés de succès :

- qualité et cohérence des trois sources ;
- choix d'un seuil métier validé avec les RH ;
- adoption par les équipes via une interface simple ;
- traçabilité des décisions pour audit et amélioration continue.

Cas d'usage priorisés :

1. scoring individuel via formulaire (usage quotidien RH) ;
2. scoring en lot via CSV (campagnes d'analyse) ;
3. monitoring des prédictions et des tendances (pilotage).

## 4. Appui stratégique et méthodologique

### 4.1 Proposition de démarche projet

J'ai structuré la démarche en étapes lisibles :

1. cadrage et compréhension des données ;
2. construction de la base et du pipeline de préparation ;
3. entraînement et évaluation du modèle ;
4. packaging et interface Gradio ;
5. déploiement, tests et documentation.

Méthodologie : une approche CRISP-DM avec itérations courtes (prototypage rapide, validation métier, itération).

### 4.2 Aide à la prise de décision

Risques et opportunités :

- opportunité : visibilité RH immédiate sur les risques de départ ;
- risque : biais potentiels et perception RH (nécessité de transparence) ;
- risque : dépendance aux données d'entrée, qualité variable des sources.

Scénarios budgétaires :

- scénario léger : stack open source locale + déploiement HF ;
- scénario renforcé : base managée + monitoring avancé + gouvernance.

KPIs proposés :

- taux d'utilisation de l'outil par les RH ;
- précision des alertes (taux de faux positifs / faux négatifs) ;
- délai de mise à jour des modèles ;
- volume et qualité des logs de prédiction.

Impacts pris en compte :

- éthique et conformité (RGPD, minimisation des données, explicabilité) ;
- organisationnel (processus RH de suivi des alertes) ;
- business (coût de l'attrition vs coût de l'intervention).

## 5. Contrôle et suivi du projet

### 5.1 Tableau de bord de pilotage

Indicateurs de suivi :

- avancement des livrables (pipeline, modèle, app, doc) ;
- qualité et fraîcheur des données ;
- performance du modèle et répartition des scores ;
- volume de prédictions par source (formulaire, CSV, bruts).

Reporting recommandé :

- hebdomadaire pour l'équipe projet ;
- mensuel pour le comité de pilotage RH/DSI.

### 5.2 Outils et process de suivi

- logs d'exécution `logs/pipeline_logs` et `logs/tests_logs` ;
- journal des prédictions en base (`prediction_logs`) ;
- tests automatisés via Pytest ;
- documentation continue via MkDocs.

## 6. Conclusion & recommandations

Ce projet part d'un besoin RH concret et aboutit à une solution opérationnelle : un pipeline data robuste, un modèle ML adapté aux données tabulaires et une interface accessible pour les équipes. Le tout est documenté et déployable rapidement.

Décisions structurantes :

- PostgreSQL pour la fiabilité et l'audit ;
- scikit-learn pour un ML lisible et efficace ;
- Gradio pour une adoption rapide et une démonstration fluide.

Prochaines étapes recommandées :

- renforcer la couverture de tests et l'explicabilité ;
- automatiser un monitoring de drift ;
- préparer une version intégrable dans le SI RH.
