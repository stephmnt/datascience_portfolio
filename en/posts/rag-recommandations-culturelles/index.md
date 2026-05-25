<!--
.. title: RAG : assistant intelligent de recommandations culturelles
.. slug: rag-recommandations-culturelles
.. description: Construire un POC RAG de bout en bout pour recommander des évènements culturels fiables en Occitanie, via une API, avec robustesse (tests, logs) et reproductibilité.
.. date: 2026-02-27 00:00:01
-->

## 0. Fil narratif du projet

Au départ, le besoin exprimé par Jérémy (responsable technique) était très concret : *"Pouvons-nous prouver rapidement qu'un assistant intelligent peut recommander des évènements culturels fiables, exploitables via API, sans lancer un grand chantier d'industrialisation ?"*

La réponse du projet a été volontairement pragmatique :

* construire un POC de bout en bout,
* limiter le périmètre à l'Occitanie pour garantir la qualité,
* privilégier la robustesse (tests, logs, reproductibilité),
* livrer une API utilisable tout de suite par les équipes produit/marketing.

Ce rapport raconte cette démarche, depuis le besoin métier jusqu'aux décisions de pilotage et aux prochaines étapes.

---

## 1. Contexte et analyse des besoins

### 1.1 Présentation

**Organisation cible :** Puls-Events, entreprise technologique orientée recommandations culturelles.

**Structure projet :**

* métier : équipes produit/marketing qui veulent un assistant testable rapidement,
* technique : responsable technique + implémentation data/ML,
* exploitation : besoin d'une API stable pour intégration future.

**Enjeux stratégiques liés à la donnée :**

* convertir un catalogue d'évènements en expérience conversationnelle utile,
* réduire le temps entre la question utilisateur et une suggestion actionnable,
* rendre les réponses auditables (sources, dates, lieux), et non "boîte noire".

**Maturité data & ML (forces / faiblesses) :**

* Forces :

  * accès à une source d'évènements (OpenAgenda),
  * vision produit claire sur l'usage final,
  * capacité à tester via API locale rapidement.
* Faiblesses :

  * qualité hétérogène des métadonnées source (notamment URLs),
  * absence initiale d'un socle ML standardisé,
  * besoin d'un cadre d'évaluation plus riche pour le passage à l'échelle.

### 1.2 Collecte et analyse du besoin métier

**Parties prenantes identifiées :**

* Jérémy (sponsor technique et arbitrage),
* équipe produit (parcours utilisateur, cas d'usage),
* équipe marketing (valeur business des recommandations),
* data scientist/ML engineer (conception et delivery),
* évaluateur final (validation des livrables et de la soutenance).

**Recueil du besoin (sources utilisées) :**

* cadrage de mission (`ressources/mission.md`),
* critères de validation (`ressources/livrables.md`),
* itérations techniques et tests automatisés (`tests/tests.py`),
* démonstration locale API (commands `app.py run-api`, `app.py api-test`).

**Hiérarchisation des besoins (priorisation MoSCoW) :**

| Niveau | Besoin                                              | Statut projet  |
| ------ | --------------------------------------------------- | -------------- |
| Must   | Réponse RAG basée sur des sources réelles           | Livre          |
| Must   | API REST `/ask`, `/rebuild`, `/health`, `/metadata` | Livre          |
| Must   | Reproductibilité et secrets hors code               | Livre          |
| Must   | Tests unitaires relançables sans réseau             | Livre          |
| Should | Interface web simple pour profils non techniques    | Livre          |
| Should | Rebuild index contrôlé (token + lock)               | Livre          |
| Could  | Évaluation avancée (RAGAS complet)                  | À planifier    |
| Could  | Personnalisation utilisateur multi-tours            | Hors scope POC |

**Contraintes métier, réglementaires et opérationnelles :**

* géographie : Occitanie,
* temporalité : évènements récents + à venir,
* sécurité : clés API via `.env` uniquement,
* robustesse : gestion des erreurs et cas limites,
* opérationnel : POC demoable localement + Docker,
* gouvernance : pas d'historique conversationnel dans ce POC.

---

## 2. Audit de la solution data existante (ou proposée)

### 2.1 Solution actuelle ou proposée

Il n'existait pas de solution RAG industrialisée préexistante. Le projet a donc construit une solution cible progressive :

**Outils et technologies :**

* collecte : OpenAgenda API,
* traitement : Python + pandas,
* indexation sémantique : FAISS CPU,
* orchestration RAG : LangChain,
* génération : Mistral,
* exposition : Flask API,
* exploitation : CLI unifiée `app.py`, tests `pytest`, conteneurisation Docker.

**Processus d'exploitation des données (pipeline) :**

1. `app.py build-dataset` -> collecte multi-agendas + nettoyage,
2. `app.py build-index` -> chunking + embeddings + index FAISS,
3. `app.py ask-local` ou `POST /ask` -> retrieval + génération,
4. `POST /rebuild` -> reload/rebuild contrôlé,
5. `app.py bootstrap` -> préparation bout-en-bout.

### 2.2 Évaluation de l'adéquation aux besoins

| Critère            | Observation                                                           | Niveau      |
| ------------------ | --------------------------------------------------------------------- | ----------- |
| Pertinence métier  | Réponses ancrées sur des évènements réels + sources                   | Bon         |
| Fiabilité          | Gestion d'erreurs API, fallback anti-hallucination, validation schema | Bon         |
| Scalabilité POC    | Rebuild local rapide, index persistant, cache mémoire                 | Correct     |
| Coût               | Stack open-source majoritaire, coût LLM pilotable                     | Bon         |
| Exploitabilité     | API claire + script de démo + logs + Docker                           | Bon         |
| Évaluation qualité | Smoke eval disponible, mais coverage sémantique à approfondir         | À renforcer |

**Écarts et limites identifiés :**

* métadonnées inégales selon agendas (URLs parfois absentes),
* distribution géographique variable selon l'activité des agendas,
* évaluation encore "smoke" (utile, mais non exhaustive).

**Visualisation simplifiée du flux existant/proposé :**

{{% mermaid %}}
flowchart LR
    A[OpenAgenda] --> B[Collecte multi-agendas]
    B --> C[Nettoyage + normalisation]
    C --> D[Dataset traité]
    D --> E[Embeddings + FAISS]
    E --> F[Retriever RAG]
    F --> G[LLM Mistral]
    G --> H[API Flask]
    H --> I[Usage métier / démo]
{{% /mermaid %}}

---

## 3. Identification d'une solution technique cible

### 3.1 Comparatif d'approches techniques

| Approche                         | Avantages                                                 | Inconvénients                          | Décision          |
| -------------------------------- | --------------------------------------------------------- | -------------------------------------- | ----------------- |
| Recherche par mots-clés + règles | Simple, peu coûteux                                       | Peu robuste au langage naturel         | Non retenue       |
| LLM seul (sans retrieval)        | Réponses fluides                                          | Risque d'invention, faible traçabilité | Non retenue       |
| Fine-tuning complet              | Potentiel qualitatif élevé                                | Coût/temps de données et entraînement  | Non retenue (POC) |
| **RAG (FAISS + LLM)**            | Équilibre fiabilité / vitesse / coût, sources explicables | Dépend de la qualité des données       | **Retenue**       |

### 3.2 Architecture cible

Architecture cible retenue :

* source externe (OpenAgenda),
* couche data prep (schema stable),
* couche indexation (FAISS persistante),
* couche génération (Mistral guidée par prompt),
* couche service (API Flask + gouvernance opératoire).

### 3.3 Facteurs clés de succès et points de vigilance

**Facteurs clés de succès :**

* discipline sur la qualité des données,
* prompt anti-hallucination explicite,
* API simple, stable, sécurisée,
* tests relançables et reproductibilité.

**Points de vigilance :**

* performance réelle sous charge (au-delà du POC),
* suivi de qualité continue des sources OpenAgenda,
* maturité de l'évaluation métrique avant scale.

### 3.4 Méthodologie d'identification et priorisation des cas d'usage

Approche retenue : priorisation Impact métier x Effort technique.

| Cas d'usage                              | Impact métier | Effort      | Priorité |
| ---------------------------------------- | ------------- | ----------- | -------- |
| Reco d'évènements généraliste (`/ask`)   | Élevé         | Moyen       | P1       |
| Supervision API (`/health`, `/metadata`) | Élevé         | Faible      | P1       |
| Rebuild opérationnel (`/rebuild`)        | Moyen/élevé   | Moyen       | P1       |
| Interface web non technique (`/app`)     | Moyen         | Faible      | P2       |
| Évaluation avancée continue              | Élevé         | Moyen/élevé | P2       |
| Personnalisation utilisateur fine        | Élevé         | Élevé       | P3       |

---

## 4. Appui stratégique et méthodologique

### 4.1 Proposition de démarche projet

**Cadre méthodologique :** CRISP-DM adapté + itérations courtes de type Agile.

**Roadmap de mise en œuvre (ce qui a été réalisé) :**

1. Cadrage & risques (scope Occitanie, contraintes secrets, périmètre API),
2. Préparation data (collecte + nettoyage + schema),
3. Indexation sémantique (chunking + embeddings + FAISS),
4. Moteur RAG (retrieval + génération + fallback),
5. API Flask robuste (validation, erreurs, auth, rebuild lock),
6. Packaging et démo (CLI unifiée + Docker + scripts de vérification).

**Responsabilités (vision simplifiée) :**

* Sponsor technique : priorisation et acceptation,
* Data/ML : conception pipeline et RAG,
* Produit/métier : validation des scénarios utilisateur,
* QA/projet : vérification des tests et des livrables.

### 4.2 Aide à la prise de décision

**Synthèse risques / opportunités :**

| Type        | Élément                                         |
| ----------- | ----------------------------------------------- |
| Opportunité | Assistant explicable et testable rapidement     |
| Opportunité | Réutilisation API directe par produit/marketing |
| Risque      | Qualité source hétérogène selon agendas         |
| Risque      | Surconfiance si métriques non enrichies         |
| Risque      | Coût variable si usage LLM non piloté           |

**Scénarios budgétaires (ordre de grandeur, 3 mois) :**

* Scénario A - POC local renforcé : 1 personne part-time, coût infra faible.
* Scénario B - Pilote métier restreint : 1 data/ML + 1 backend part-time + supervision qualité.
* Scénario C - Pré-industrialisation : équipe pluridisciplinaire (data, backend, produit, QA), observabilité et MLOps renforcés.

**KPI de succès recommandés :**

* KPI business :

  * taux d'utilisation de `/ask`,
  * taux de réponses jugées utiles par les testeurs métier,
  * temps moyen de réponse ressenti acceptable.
* KPI techniques :

  * latence médiane API,
  * taux d'erreur 4xx/5xx,
  * couverture tests,
  * part de réponses avec sources exploitables.

**Impacts et conformité dans les recommandations :**

* Éthique : éviter l'invention (fallback explicite),
* Légal/réglementaire : aucune clé en dur, secrets hors git,
* Organisationnel : clarifier la responsabilité "qualité data source",
* Business : privilégier fiabilité et explicabilité avant extension fonctionnelle.

---

## 5. Contrôle et suivi du projet

### 5.1 Tableau de bord de pilotage

**Indicateurs de suivi recommandés :**

* Délai : avancement par étape (data, index, rag, api, démo),
* Qualité livraison : statut tests (`pytest`),
* Qualité data : nombre d'évènements valides / invalides,
* Qualité réponse : score smoke eval + revue métier,
* Opérations : disponibilité API (`/health`) et metadata index (`/metadata`).

**Fréquence et mode de reporting :**

* quotidien en phase de construction (point court),
* hebdomadaire en phase de stabilisation,
* revue de sprint avec démonstration fonctionnelle.

### 5.2 Outils et process de suivi

**Suivi expérimentation / delivery :**

* CLI unifiée `app.py` pour standardiser les exécutions,
* logs (`logs/`) pour diagnostics,
* rapport smoke eval (`reports/smoke_eval_report.json`) pour comparaison rapide,
* tests unitaires centralisés (`tests/tests.py`).

**Gestion projet & collaboration :**

* gestion de versions Git avec branches explicites par étape,
* Definition of Done : code + tests + doc + commande de vérification,
* trace des décisions techniques dans README + rapports de soutenance.

---

## 6. Conclusion & recommandations

### 6.1 Récapitulatif des décisions prises

* Choix RAG retenu pour allier pertinence métier et explicabilité,
* Scope Occitanie pour maîtriser la qualité dans le POC,
* API Flask choisie pour exposition simple et robuste,
* Priorité donnée à la reproductibilité et aux tests relançables.

### 6.2 Perspectives d'évolution

* enrichir la qualité source (notamment URLs),
* étendre l'évaluation au-delà du smoke test,
* renforcer l'observabilité (SLA, tracing, qualité par territoire),
* ouvrir progressivement à des cas d'usage plus personnalisés.

### 6.3 Prochaines étapes recommandées (30 / 60 / 90 jours)

**J+30 :**

* stabiliser qualité data et tableau de bord KPI minimum
* finaliser protocole d'évaluation métier/technique.

**J+60 :**

* lancer pilote métier avec panel d'utilisateurs internes,
* ajuster prompts, filtres et priorisation retrieval.

**J+90 :**

* arbitrer passage pré-industrialisation (coût/risque/ROI),
* formaliser plan cible MLOps et gouvernance data.

---

## Synthèse

Le projet a transformé un besoin métier clair - recommander vite et fiable des évènements culturels - en un POC RAG complet, testable et exploitable via API. Le choix technique est cohérent avec le niveau de maturité visé : robuste, explicable, reproductible. La principale limite n'est pas l'architecture, mais la qualité hétérogène de certaines données source ; c'est donc le premier levier d'amélioration pour maximiser la valeur business lors du passage à l'échelle.
