<!--
.. title: RAG : fiabiliser un assistant intelligent
.. slug: rag-assistant-hybride-usage-metier
.. description: Transformer un prototype RAG + SQL en un système métier plus fiable, mesurable et reproductible, avec API, évaluation RAGAS, validations et pilotage projet.
.. date: 2026-03-18 00:00:01
-->

# Rapport de conduite de projet

## Fiabiliser un assistant RAG NBA pour un usage métier

Ce projet commence comme beaucoup de projets data appliqués : avec une promesse forte et un prototype encore fragile.

SportSee dispose d’un assistant capable de répondre à certaines questions sur des données NBA. Le prototype est encourageant, mais il ne suffit pas encore pour un usage métier. Les coachs et analystes n’attendent pas seulement une réponse "plausible". Ils ont besoin d’une réponse utile, traçable, reproductible et défendable.

L’objectif du projet a donc été reformulé de manière simple : transformer un prototype RAG intéressant en un système compréhensible, testable et pilotable.

---

## 1. Contexte et analyse des besoins

### 1.1 Présentation de l’organisation et du contexte

SportSee est présentée comme une startup spécialisée dans l’IA appliquée à l’analyse de la performance sportive. Son positionnement se situe à l’intersection de trois mondes :

- la donnée sportive structurée ;
- les archives textuelles d’analyse ;
- l’intelligence artificielle générative au service des équipes métiers.

Le contexte est celui d’une organisation agile, orientée produit, avec une maturité data intermédiaire :

- point fort : l’entreprise a déjà un prototype, un corpus, et un cas d’usage métier clair ;
- point faible : le prototype n’est pas encore assez robuste pour une mise en production ou une diffusion à d’autres clubs ;
- enjeu stratégique : gagner du temps d’analyse, fiabiliser les réponses, et rendre le système crédible pour des utilisateurs non techniques.

Le projet ne porte donc pas seulement sur la performance du modèle. Il porte sur la confiance dans la chaîne complète : données, retrieval, SQL, génération, évaluation et documentation.

### 1.2 Collecte et analyse du besoin métier

Le besoin métier a été reconstitué à partir de plusieurs sources :

- le cadrage de mission ;
- les échanges fictifs avec Sarah, Data Scientist de l’équipe ;
- les exemples de questions métier fournis dans le scénario ;
- l’audit du prototype existant et de son comportement réel.

Les parties prenantes principales sont les suivantes :

- Sarah, Data Scientist, qui porte la fiabilisation du prototype ;
- l’équipe R&D, qui maintient l’assistant ;
- les coachs, analystes vidéo et préparateurs physiques, futurs utilisateurs ;
- plus largement, les décideurs métiers qui doivent juger si l’outil est assez fiable pour être utilisé.

Les besoins ont été hiérarchisés en trois niveaux.

| Priorité | Besoin | Pourquoi c’est critique |
| --- | --- | --- |
| Haute | Répondre correctement aux questions textuelles et chiffrées | C’est la valeur métier directe du produit |
| Haute | Mesurer la qualité réelle du système | Sans évaluation, impossible de décider d’un passage en production |
| Haute | Reproduire l’environnement et documenter le pipeline | Condition de continuité, de maintenance et de crédibilité |
| Moyenne | Visualiser et suivre les performances dans le temps | Important pour le pilotage et la soutenance |
| Moyenne | Mieux gérer les cas limites et les questions hybrides | Important pour la robustesse métier |
| Faible à moyenne | Industrialiser davantage l’observabilité et le monitoring | Utile à moyen terme, moins critique que la fiabilité de base |

Les contraintes identifiées sont à la fois métiers, techniques et opérationnelles :

- les réponses doivent rester compréhensibles pour un profil non technique ;
- les données textuelles et structurées doivent être cohérentes entre elles ;
- certaines données attendues ne sont pas présentes dans le corpus, ce qui impose au système de savoir dire "je ne sais pas" ;
- la chaîne dépend d’outils externes, notamment pour la génération et, potentiellement, pour l’OCR ;
- le projet doit rester démontrable dans un repo clair, simple à exécuter et à auditer.

---

## 2. Audit de la solution data existante

### 2.1 Solution actuelle ou proposée

Au départ, la solution ressemble à un prototype RAG classique enrichi progressivement :

- un corpus de documents indexés dans FAISS ;
- des données NBA structurées chargées dans SQLite ;
- un assistant capable de combiner retrieval et génération ;
- un outillage SQL pour les questions chiffrées ;
- un script d’évaluation basé sur RAGAS ;
- une interface Streamlit et une API FastAPI.

Le pipeline actuel peut être résumé ainsi :

{{% mermaid %}}
flowchart LR
    A[Sources Excel et PDF] --> B[Préparation des données]
    B --> C[Index FAISS]
    B --> D[Base SQLite]
    C --> E[Service RAG + SQL]
    D --> E
    E --> F[API / Streamlit]
    E --> G[Évaluation RAGAS]
    G --> H[Notebook de rapport]
{{% /mermaid %}}

Cette architecture a un mérite important : elle couvre tout le cycle de vie d’un système data appliqué, de l’ingestion jusqu’à l’analyse des résultats.

### 2.2 Évaluation de l’adéquation aux besoins

L’audit montre un constat nuancé.

La solution répond bien à plusieurs attentes :

- elle traite des questions documentaires ;
- elle sait mobiliser une base SQL pour les questions quantitatives ;
- elle dispose d’un dispositif d’évaluation explicite ;
- elle a été structurée pour devenir plus reproductible et plus lisible.

Mais les écarts initiaux étaient réels :

- le prototype était plus convaincant sur les questions simples que sur les cas hybrides ;
- les performances globales n’étaient pas suffisantes pour conclure à une robustesse générale ;
- l’évaluation devait être mieux reliée à des cas d’usage métier ;
- l’observabilité et la validation des flux de données demandaient à être renforcées ;
- l’OCR s’est révélé instable sur la stack locale, ce qui a obligé à privilégier un mode de fonctionnement sûr plutôt qu’un mode "plus ambitieux mais fragile".

Les critères retenus pour juger l’adéquation de la solution ont été :

- la pertinence des réponses ;
- la fidélité au contexte ;
- la qualité du retrieval ;
- la capacité à répondre aux questions chiffrées ;
- la traçabilité du pipeline ;
- la facilité de réexécution du projet ;
- la lisibilité du livrable pour un tiers.

En synthèse, la solution est adaptée à une phase de démonstration sérieuse et d’audit méthodologique, mais elle n’est pas encore une solution de production industrialisée.

---

## 3. Identification d’une solution technique cible

Le choix de la cible n’a pas été guidé par la sophistication maximale. Il a été guidé par l’équilibre entre utilité métier, robustesse et clarté.

Trois approches ont été comparées.

| Approche | Avantages | Limites |
| --- | --- | --- |
| RAG seul | Simple à comprendre, bon pour la recherche documentaire | Faible dès qu’il faut comparer ou calculer des chiffres |
| SQL seul | Très bon pour les données structurées et les agrégations | Incapable de répondre seul sur les contenus textuels |
| RAG + SQL + évaluation | Meilleure couverture métier, plus défendable, plus pilotable | Plus complexe à concevoir et à tester |

La solution cible retenue est donc une architecture hybride :

- retrieval documentaire pour les contenus textuels ;
- base SQL pour les chiffres ;
- service partagé pour orchestrer les deux ;
- Pydantic pour valider les objets qui circulent ;
- RAGAS et métriques complémentaires pour objectiver la qualité ;
- notebook de rapport pour interpréter les résultats.

### Architecture cible

{{% mermaid %}}
flowchart TD
    U[Utilisateur métier] --> A[API / Streamlit]
    A --> B[Service RAGService]
    B --> C[Retriever FAISS]
    B --> D[Tool SQL]
    B --> E[Mistral]
    C --> F[Corpus documentaire]
    D --> G[SQLite NBA]
    B --> H[Réponse contrôlée]
    H --> I[Évaluation RAGAS]
    I --> J[Rapport et pilotage]
{{% /mermaid %}}

### Facteurs clés de succès

- garder un service partagé unique pour éviter les comportements divergents ;
- valider explicitement les flux de données ;
- traiter séparément les cas simples, complexes, bruités et hybrides ;
- documenter les limites plutôt que masquer les échecs ;
- rester sobre techniquement pour garder un repo compréhensible.

### Points de vigilance

- les métriques automatiques ne suffisent pas à elles seules ;
- le mapping langage naturel vers SQL reste une zone sensible ;
- la qualité du corpus conditionne fortement la qualité des réponses ;
- l’OCR n’est pas aujourd’hui un composant stable sur la stack locale ;
- un bon score moyen peut masquer des échecs critiques sur certains cas d’usage.

### Priorisation des cas d’usage

La priorisation des cas d’usage s’est faite selon deux axes :

- valeur métier ;
- difficulté technique.

Les cas d’usage prioritaires sont :

1. retrouver une information simple sur une équipe ou un joueur ;
2. répondre à une question chiffrée fiable ;
3. gérer les questions hybrides texte + chiffres ;
4. reconnaître honnêtement les limites du corpus.

---

## 4. Appui stratégique et méthodologique

### 4.1 Proposition de démarche projet

La démarche la plus pertinente pour ce projet est une approche hybride entre CRISP-DM et gestion agile.

CRISP-DM apporte un cadre utile :

- compréhension métier ;
- compréhension des données ;
- préparation des données ;
- modélisation ;
- évaluation ;
- déploiement.

L’agilité apporte le rythme :

- itérations courtes ;
- revue régulière des résultats ;
- arbitrages rapides entre valeur et risque ;
- capacité à corriger la documentation et le code en continu.

### Roadmap de mise en œuvre

| Phase | Objectif | Livrables |
| --- | --- | --- |
| Phase 1 | Stabiliser l’environnement | `requirements.txt`, README, arborescence claire |
| Phase 2 | Structurer les données | indexation, base SQLite, pipeline d’ingestion |
| Phase 3 | Fiabiliser la chaîne de réponse | service partagé, tool SQL, validations |
| Phase 4 | Mesurer objectivement | `evaluate_ragas.py`, jeux de questions, artefacts |
| Phase 5 | Interpréter et piloter | notebook, comparatifs, storytelling de soutenance |

### 4.2 Aide à la prise de décision

Le projet présente plusieurs opportunités :

- gagner du temps côté analystes ;
- réduire les réponses arbitraires ou difficiles à justifier ;
- disposer d’un socle réutilisable pour d’autres sports ou d’autres clubs ;
- installer une culture de mesure autour des systèmes d’IA générative.

Les principaux risques sont :

- surconfiance dans les réponses du modèle ;
- sous-estimation des cas hybrides ;
- dépendance à des services externes ;
- qualité inégale des sources textuelles ;
- coût de maintenance si l’architecture devient trop complexe.

### Scénarios budgétaires indicatifs

Ces estimations sont volontairement simples et servent surtout à la décision.

| Scénario | Périmètre | Coût indicatif |
| --- | --- | --- |
| Minimal | usage local, API + notebook + tests | faible |
| Pilote | équipe métier restreinte, suivi mensuel, support basique | moyen |
| Industrialisation | supervision renforcée, monitoring continu, support multi-clubs | élevé |

Les principaux postes de coût sont :

- appels API LLM / embeddings ;
- temps d’ingénierie et de maintenance ;
- hébergement de l’API et de l’interface ;
- monitoring et support ;
- travail de gouvernance documentaire et de qualification des cas de test.

### Indicateurs de succès

Les KPI doivent rester lisibles pour les métiers.

KPI business :

- temps gagné pour retrouver une information ;
- taux de réponses jugées utiles par les utilisateurs ;
- réduction des réponses non exploitables ;
- fréquence d’usage de l’assistant.

KPI techniques :

- answer relevancy ;
- faithfulness ;
- précision et rappel du retrieval ;
- latence moyenne ;
- taux de questions où SQL est correctement mobilisé ;
- taux de cas limites correctement reconnus comme non couverts.

### Impacts éthiques, légaux et organisationnels

Le projet ne manipule pas ici de données médicales sensibles, mais il touche à la performance sportive et à des usages décisionnels. Il faut donc :

- éviter de présenter une réponse générée comme une vérité garantie ;
- conserver la traçabilité des sources ;
- prévoir une relecture humaine pour les décisions importantes ;
- garder une gouvernance claire sur les données utilisées et partagées.

---

## 5. Contrôle et suivi du projet

### 5.1 Tableau de bord de pilotage

Le projet peut être piloté avec un tableau de bord simple, lisible par un binôme métier / technique.

| Axe | Indicateurs |
| --- | --- |
| Avancement | jalons atteints, scripts livrés, documentation à jour |
| Qualité data | taux de sources exploitables, complétude du corpus, incidents OCR |
| Qualité IA | scores RAGAS, métriques retrieval, cas faibles identifiés |
| Robustesse | tests verts, validations Pydantic, stabilité des runs |
| Usage | questions fréquentes, retours métier, cas non couverts |

Fréquence recommandée :

- point rapide hebdomadaire en phase de construction ;
- revue d’évaluation à chaque nouvelle campagne de tests ;
- point mensuel si le système entre en phase pilote.

### 5.2 Outils et process de suivi

Les outils et pratiques déjà cohérents avec le projet sont :

- Git et GitHub pour la version du code ;
- README pour la documentation d’exploitation ;
- notebook de rapport pour la lecture métier des résultats ;
- sorties `outputs/evaluations/` pour historiser les runs ;
- Logfire, quand il est activé, pour suivre le comportement du pipeline ;
- tests et validations Pydantic comme garde-fous de qualité.

Le bon process n’est pas de produire plus d’outils. C’est de ritualiser leur usage :

- un lot de questions de référence stable ;
- une réévaluation après chaque changement important ;
- une lecture conjointe des scores et des cas d’échec ;
- une décision explicite sur ce qui est acceptable, fragile ou insuffisant.

---

## 6. Conclusion et recommandations

Ce projet raconte une trajectoire assez classique, mais saine : partir d’un prototype séduisant, puis accepter de le regarder de façon critique pour le rendre crédible.

Les décisions structurantes prises dans le projet sont les suivantes :

- retenir une architecture hybride RAG + SQL ;
- privilégier la validation et la traçabilité plutôt qu’une complexité inutile ;
- évaluer le système avec des cas d’usage métier variés ;
- documenter explicitement les limites ;
- construire un repo défendable en soutenance comme en reprise technique.

### Recommandations prioritaires

1. Stabiliser le corpus réellement exploitable, en particulier sur les documents OCR.
2. Continuer à enrichir les cas de test hybrides et bruités.
3. Conserver une lecture métier des scores, pas seulement une lecture technique.
4. Maintenir un service partagé unique pour éviter les divergences entre API, UI et évaluation.
5. Utiliser les résultats d’évaluation comme outil d’arbitrage produit, pas seulement comme livrable académique.

### Perspectives d’évolution

- améliorer la couverture OCR avec une solution plus stable ;
- renforcer le monitoring longitudinal des performances ;
- ouvrir la voie à d’autres sports ou d’autres sources ;
- intégrer à terme des visualisations automatiques ou des outils de restitution plus avancés.

En résumé, le projet ne se limite pas à "faire répondre un LLM". Il montre comment cadrer, mesurer, expliquer et piloter un système d’IA appliqué à un besoin métier concret. C’est cette capacité de pilotage, plus encore que la seule réponse générée, qui donne au projet sa valeur réelle.

{{% mermaid %}}
flowchart TD
    U[Utilisateur] -->|Question| S[Streamlit MistralChat.py]
    U -->|HTTP JSON| A[FastAPI api.py]

    S --> G[Service partagé RAGService api.py]
    A --> G

    G --> R[Retriever FAISS utils/vector_store.py]
    G --> T[Tool SQL sql_tool.py]
    G --> M[Mistral API]

    R --> V[(vector_db/faiss_index.idx + document_chunks.pkl)]
    T --> D[(database/nba_data.db)]

    I[indexer.py] --> V
    L[load_excel_to_db.py] --> D

    E[evaluate_ragas.py] --> R
    E --> T
    E --> M
    E --> O[(outputs/evaluations)]

    N[rapport_evaluation.ipynb] --> O
{{% /mermaid %}}