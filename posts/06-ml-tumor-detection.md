<!--
.. title: Classification d’images médicales
.. slug: imagerie-medicale-non-semi-supervise
.. description: Exploiter un grand volume d’images non labellisées pour distinguer “cancer” vs “normal”, réduire l’effort d’annotation et préparer le passage à l’échelle.
.. date: 2026-02-01 00:00:01
-->

# Rapport de conduite de projet Data & ML — Classification d’images médicales (approches non & semi-supervisées)

> Tout est parti d’un constat simple : en imagerie médicale, on a souvent beaucoup d’images, mais trop peu de temps médical pour tout annoter correctement. Plutôt que d’attendre une campagne de labellisation parfaite, on a choisi une trajectoire progressive. D’abord, on apprend à “résumer” chaque image sous forme d’un vecteur de caractéristiques (des embeddings) afin d’avoir une représentation comparable et réutilisable. Ensuite, on organise les images non labellisées grâce au clustering pour mieux comprendre la structure du dataset. Enfin, on transforme une partie de cet “inconnu” en signal exploitable via des pseudo-labels, afin d’améliorer la classification tout en limitant l’effort d’annotation.

---

## 1. Contexte et analyse des besoins

### 1.1 Présentation (organisation et / ou contexte)

Le projet s’inscrit dans le secteur de la santé, plus précisément dans le domaine de l’imagerie médicale. L’objectif opérationnel est de produire un modèle de classification binaire capable de distinguer des images “cancer” de celles considérées comme “normal”. L’enjeu est d’apporter une aide à la décision et au tri, sans se positionner comme un outil de diagnostic automatisé. Le jeu de travail mis à disposition comprend un petit socle d’images labellisées, au total cent images réparties équitablement entre les deux classes, ainsi qu’un volume bien plus important d’images non labellisées, au nombre de 1406. Les images sont homogènes en taille, ce qui simplifie la standardisation du pipeline et limite une partie des problèmes de qualité de données.

Sur le plan stratégique, ce projet vise surtout à réduire la dépendance à l’annotation manuelle, qui est coûteuse, rare et lente, tout en capitalisant sur la valeur du stock d’images non labellisées, généralement majoritaire dans les contextes de santé. La démarche retenue prépare également le passage à l’échelle : l’idée est de mettre en place une chaîne qui reste pertinente même lorsque la volumétrie augmente fortement.

En termes de maturité data & ML, le projet bénéficie d’une structuration simple des données, déjà séparées entre labellisé et non labellisé, et d’un équilibre des classes du côté labellisé. En revanche, la faiblesse principale reste la taille très limitée du dataset annoté, ce qui fragilise l’évaluation et augmente le risque de sur-apprentissage. Il existe aussi un risque de biais lié à la provenance des images et aux conditions d’acquisition, qui peuvent limiter la généralisation si le contexte de production diffère.

### 1.2 Collecte et analyse du besoin métier

Le cadrage métier s’appuie sur une identification claire des parties prenantes. Les médecins et radiologues apportent la définition clinique du besoin, les critères d’acceptation et la validation des erreurs jugées tolérables. Les responsables métier ou produit cadrent la priorisation, l’intégration dans le parcours de travail et les attentes d’adoption. Les profils data et ML construisent les approches, organisent l’évaluation et pilotent les itérations. Les équipes data engineering assurent la robustesse du pipeline, le stockage et les questions de performance. Enfin, la conformité et la sécurité sont cadrées avec les interlocuteurs DPO et RSSI, compte tenu des exigences RGPD.

Le recueil du besoin s’est construit de manière pragmatique à partir de la mission et des livrables attendus, puis consolidé dans une logique d’ateliers de cadrage portant sur les objectifs, les contraintes, les critères de succès et les risques, à la fois techniques et réglementaires. Un PoC itératif a ensuite permis d’objectiver rapidement la faisabilité et de mettre des métriques sur le problème, en complément d’une analyse d’erreurs orientée métier.

La hiérarchisation des besoins suit une logique impact/effort. La première priorité est d’obtenir une baseline fiable sur la classification “cancer” versus “normal” avec un pipeline reproductible, de manière à sécuriser la valeur et la trajectoire. La deuxième priorité est d’exploiter les données non labellisées via des mécanismes semi-supervisés pour limiter la charge d’annotation. La troisième priorité est de préparer l’industrialisation, en particulier la traçabilité, le versioning des artefacts et le suivi des performances dans le temps.

Pour couvrir l’ensemble des dimensions pertinentes, le projet prend en compte à la fois la performance (avec des métriques adaptées comme la F1-score, la ROC-AUC, la matrice de confusion et un focus sur le rappel de la classe “cancer”), la robustesse (stabilité sur le test, sensibilité aux paramètres, analyse d’erreurs), la gouvernance (traçabilité, conformité, sécurisation, documentation) et l’opérationnel (coûts de calcul, fréquence de mise à jour, intégration dans les pratiques métier).

Les contraintes à intégrer sont fortes : il s’agit de données de santé, donc la conformité RGPD impose une logique de minimisation, de contrôle d’accès, de journalisation et de maîtrise de la conservation. De plus, puisque le modèle est une aide, il faut éviter la sur-confiance et privilégier le rappel ou la sensibilité quand le contexte clinique le nécessite, en limitant autant que possible les faux négatifs. Enfin, le projet vise des solutions sobres au début, en privilégiant des représentations réutilisables et des modèles légers avant d’envisager des stratégies plus coûteuses comme le fine-tuning.

---

## 2. Audit de la solution data existante (ou proposée si absence de solution existante)

### 2.1 Solution actuelle ou proposée

L’état initial correspond à un stockage sous forme de fichiers, avec une séparation claire entre images labellisées et non labellisées. Il n’existe pas encore de pipeline ML industrialisé ; le projet a donc pour rôle de bâtir progressivement une solution cible à partir d’un PoC structurant.

Les technologies mobilisées dans le PoC reposent sur l’écosystème Python. Elles combinent des bibliothèques de manipulation de données pour structurer et tracer les expériences, un framework deep learning pour extraire des représentations visuelles via un modèle pré-entraîné, et des outils de machine learning classiques pour la réduction de dimension, le clustering et la classification. Les artefacts produits sont exportés dans des formats adaptés au travail itératif afin de réutiliser facilement les features sans devoir recalculer tout le pipeline à chaque itération.

Le processus d’exploitation des données s’organise en trois étapes principales. La première étape consiste à réaliser un contrôle qualité, en vérifiant la lecture des images, leur cohérence et quelques statistiques simples. La deuxième étape applique des prétraitements cohérents avec le modèle pré-entraîné choisi. La troisième étape extrait des embeddings à l’aide d’un ResNet18 pré-entraîné, en retirant la couche de classification finale afin de récupérer un vecteur de représentation. Ces embeddings sont ensuite stockés et associés à une traçabilité minimale, incluant le chemin du fichier et, lorsque disponible, le label.

### 2.2 Évaluation de l’adéquation aux besoins

L’adéquation de la solution PoC aux besoins se mesure d’abord sur la performance, avec des métriques robustes et comparables dans le temps, comme la F1-score, la ROC-AUC et les matrices de confusion, en gardant une attention particulière sur la classe “cancer”. Elle se mesure également sur la capacité à passer à l’échelle, puisque l’extraction d’embeddings peut être batchée sur CPU ou GPU et qu’une fois les embeddings stockés, le ré-entraînement de modèles légers devient rapide. Le coût est un critère clé : l’approche privilégie la vitesse et l’itération plutôt que la sophistication prématurée. Enfin, la pertinence métier se juge à travers l’analyse d’erreurs, notamment l’identification et la compréhension des faux négatifs.

L’audit met en évidence plusieurs limites. La première est la fragilité statistique liée au faible volume d’images labellisées, ce qui peut gonfler artificiellement les métriques et rendre la généralisation incertaine. La deuxième est que le clustering ne dispose pas de vérité terrain sur l’unlabeled, ce qui impose de s’appuyer sur des indicateurs proxy et des contrôles qualitatifs. La troisième est le risque inhérent à la pseudo-labellisation : si les pseudo-labels sont bruités, ils peuvent amplifier des erreurs au lieu d’aider le modèle.

**Visualisation des flux / processus existants (PoC)**

{{% mermaid %}}
flowchart TD
  A["Images<br/>(labellisées + non labellisées)"] --> B["Contrôles qualité (QC)"]
  B --> C["Extraction d’embeddings<br/>(ResNet18 pré-entraîné)<br/>→ vecteur 512D"]
  C --> D["Stockage des features (versionnées)<br/>+ traçabilité (path, label)"]
  D --> E["Modélisation (baseline)"]
  D --> F["Clustering"]
  D --> G["Pseudo-labellisation (semi-sup)"]
{{% /mermaid %}}

---

## 3. Identification d’une solution technique cible

La solution technique cible se construit autour d’un comparatif d’approches. La première approche, retenue pour démarrer, consiste à exploiter des embeddings issus d’un modèle pré-entraîné, puis à entraîner un modèle classique de classification. Cette approche est rapide, peu coûteuse, itérative et relativement facile à analyser, ce qui en fait un excellent socle de démarrage. Elle peut néanmoins rencontrer un plafond de performance si les embeddings ne capturent pas suffisamment un signal clinique fin.

La deuxième approche, explorée en phase suivante, est la semi-supervision via pseudo-labellisation après clustering. Elle permet d’exploiter la masse de données non labellisées et de réduire l’effort d’annotation. En contrepartie, elle est sensible à la qualité des clusters et peut renforcer des erreurs si la stratégie de filtrage et de confiance n’est pas maîtrisée.

La troisième approche, envisagée comme un levier de performance si le ROI est confirmé, consiste à fine-tuner un modèle deep sur les données. Elle offre un potentiel supérieur, mais demande plus de labels, de ressources de calcul et une démarche de validation plus lourde.

Dans cette logique, la stratégie recommandée est de démarrer sobrement avec embeddings et modèle léger pour sécuriser rapidement la valeur. La semi-supervision est activée lorsque la qualité des pseudo-labels est suffisante et que l’on dispose d’un cadre d’évaluation robuste. Le fine-tuning est conservé comme un levier d’optimisation, à déclencher après consolidation des données, de la gouvernance et des retours métier.

**Schéma d’architecture cible clair**

{{% mermaid %}}
flowchart TD
  A["Sources images"] --> B["Ingestion / anonymisation<br/>(si nécessaire)"]
  B --> C["Data Lake"]

  A --> D["QC & Data quality report"]
  D --> E["Tableau de bord qualité"]

  A --> F["Extraction embeddings (batch)"]
  F --> G["Feature Store<br/>(embeddings)"]

  G --> H["Clustering + pseudo-labels<br/>(+ confiance)"]
  H --> I["Jeux d’entraînement enrichis"]

  I --> J["Training + évaluation"]
  J --> K["Model Registry"]

  K --> L["Déploiement (API / batch)<br/>+ monitoring"]
  L --> M["Usage métier<br/>& amélioration continue"]
{{% /mermaid %}}

Les facteurs clés de succès reposent sur la capacité à versionner les embeddings pour accélérer fortement les itérations, à standardiser les métriques et l’analyse d’erreurs, et à cadrer clairement l’usage clinique comme une aide nécessitant une validation humaine. Les points de vigilance concernent le risque de biais et de dérive dans le temps, le bruit introduit par des pseudo-labels de mauvaise qualité, et la conformité RGPD, qui impose un haut niveau de traçabilité et de sécurisation.

La priorisation des cas d’usage suit une logique simple : identifier les points de friction où l’automatisation apporte une valeur immédiate, comme le tri ou le pré-classement, puis évaluer via un PoC sur un périmètre limité avec des métriques cliniques pertinentes, et enfin prioriser en croisant impact, effort, risques et adoption. Dans ce cadre, le tri et le pré-classement constituent généralement un premier jalon à faible friction, l’aide au second avis apporte un impact fort avec un contrôle humain, et l’automatisation plus avancée ne devient réaliste que lorsque la maturité du dispositif et la validation sont suffisantes.

---

## 4. Appui stratégique et méthodologique

### 4.1 Proposition de démarche projet

La démarche projet recommandée combine CRISP-DM pour structurer les étapes et Agile pour livrer par incréments. Le cadrage sert à définir les objectifs, les métriques cibles, la gouvernance et le plan d’évaluation. La phase baseline met en place le pipeline de qualité, l’extraction d’embeddings, un modèle léger et une analyse d’erreurs. La phase semi-supervisée explore le clustering, la pseudo-labellisation, la stratégie de filtrage et la robustesse. L’industrialisation consolide le versioning, le registre de modèles, le monitoring et la documentation. Enfin, l’amélioration continue introduit un plan d’annotation ciblée, des boucles de retour terrain et le passage à l’échelle.

### 4.2 Aide à la prise de décision

Du côté des opportunités, l’approche permet d’exploiter rapidement l’unlabeled, d’itérer à faible coût et de construire une trajectoire de scaling. Les risques sont principalement liés au bruit des pseudo-labels, à la fragilité statistique d’un petit dataset labellisé, ainsi qu’aux biais et à la dérive si la distribution des images évolue.

Sur le plan budgétaire, un scénario de sobriété peut suffire au démarrage, en s’appuyant sur des embeddings et des modèles légers. Un scénario hybride devient pertinent lorsque l’on met en place la semi-supervision et un plan d’active learning pour maximiser la valeur de l’annotation. Un scénario orienté performance, incluant du fine-tuning et un MLOps plus complet, se justifie surtout lorsque l’usage métier est validé et que la gouvernance est stabilisée.

Les indicateurs de succès doivent articuler KPI business et KPI techniques. Côté business, on suivra par exemple le temps gagné, l’acceptation par les utilisateurs, la réduction du backlog et la satisfaction. Côté technique, on suivra la F1-score, la ROC-AUC, le rappel de la classe “cancer”, le taux de faux négatifs et la stabilité des performances dans le temps.

Enfin, la prise en compte des impacts éthiques, légaux et organisationnels est structurante. Éthiquement, il faut limiter la sur-confiance et documenter les limites. Légalement, la conformité RGPD impose des règles strictes d’accès, de journalisation et de conservation. Organisationnellement, il faut prévoir la formation, le changement de pratiques et un mécanisme de retour terrain.

---

## 5. Contrôle et suivi du projet

### 5.1 Tableau de bord de pilotage

Le pilotage du projet repose sur un tableau de bord couvrant le suivi des délais, des jalons, des risques et des dépendances, ainsi que la visibilité sur les coûts, notamment la consommation de calcul lors de l’extraction batch des embeddings et la charge équipe. Le suivi des livrables porte sur la complétude, la qualité, la relecture et la validation. La qualité des données est mesurée par des indicateurs comme le taux d’images valides, la présence de duplicats et des signaux de dérive. Enfin, la qualité modèle est suivie via des métriques standardisées, des matrices de confusion, des métriques centrées “cancer” et des indicateurs de calibration.

Le reporting peut être organisé avec un point hebdomadaire pour les décisions et les risques, une revue de fin de sprint centrée sur les résultats et l’analyse d’erreurs, et un comité mensuel de gouvernance incluant sécurité, RGPD et validation.

### 5.2 Outils et process de suivi

Le suivi des expérimentations s’appuie sur un outil de tracking afin de journaliser les runs, les métriques et les paramètres, et sur une discipline de reproductibilité incluant les seeds, les versions de données, le code et les dépendances. La validation est facilitée par une documentation de type “model card” qui décrit l’usage prévu, les limites, les risques et les conditions de surveillance.

Le suivi projet et la collaboration reposent sur un outil de backlog et de planification, complété par une base documentaire centralisée. Le code est versionné dans Git, les artefacts data et modèles peuvent être suivis via un outil de versioning adapté, et une CI/CD minimale est recommandée pour sécuriser les tests du pipeline et les validations avant mise en production.

---

## 6. Conclusion & recommandations

Les choix structurants du projet consistent à démarrer par une approche sobre, combinant embeddings pré-entraînés et modèle léger, puis à explorer la semi-supervision via clustering et pseudo-labellisation pour exploiter efficacement l’unlabeled. En parallèle, la mise en place d’un socle de traçabilité et de versioning est prioritaire pour rendre les itérations rapides et auditables.

Les perspectives d’évolution passent par un enrichissement progressif du labellisé, idéalement via une annotation ciblée, par un renforcement de la robustesse grâce à des schémas d’évaluation plus solides et des tests de dérive, et par l’activation du fine-tuning uniquement si le ROI est démontré et si le cadre de validation est suffisamment mature.

Les prochaines étapes recommandées s’enchaînent naturellement : consolider l’évaluation et l’analyse d’erreurs avec un focus clinique, améliorer la qualité des pseudo-labels en travaillant les méthodes, les seuils et les contrôles, déployer un socle MLOps minimal pour versionner embeddings et modèles et standardiser le monitoring, lancer une boucle d’active learning pour annoter “ce qui apporte le plus”, puis préparer le passage à l’échelle en industrialisant l’extraction batch et le stockage des représentations.