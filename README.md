# Datascience Portfolio (Nikola)

[![Déploiement Nikola](https://img.shields.io/github/actions/workflow/status/stephmnt/datascience_portfolio/deploy.yml?branch=main&label=d%C3%A9ploiement&logo=githubactions&logoColor=white)](https://github.com/stephmnt/datascience_portfolio/actions/workflows/deploy.yml)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](requirements.txt)
[![Licence](https://img.shields.io/github/license/stephmnt/datascience_portfolio?color=success)](LICENSE)

Ce dépôt contient le code source d'un portfolio statique généré avec Nikola.
Le site présente mon parcours de reconversion vers la data science et regroupe
des projets de machine learning, deep learning, NLP, RAG, MLOps et data
visualisation.

Documentation officielle Nikola : [https://getnikola.com](https://getnikola.com)
Fichier de configuration principal : `conf.py`

## Objectif du site

Le portfolio sert à documenter des projets data de bout en bout : contexte
métier, choix techniques, résultats, limites, déploiement et liens vers les
dépôts GitHub associés.

Le contenu est organisé autour de trois niveaux :

- une page d'introduction au parcours et aux compétences ;
- des rapports de projets publiés comme posts Nikola ;
- des pages complémentaires, comme le diagramme de compétences.

## Structure utile du dépôt

- `conf.py` : configuration Nikola, thème, langues, GitHub Pages et métadonnées GitHub ;
- `posts/` : rapports de projets et pages éditoriales publiées comme posts ;
- `pages/` : pages indépendantes ;
- `files/` : fichiers statiques copiés à la racine du site généré, dont `site.webmanifest` ;
- `paradigm-shift/` : thème Nikola local adapté depuis HTML5 UP Paradigm Shift ;
- `plugins/` : plugins Nikola locaux créés pour ce portfolio ;
- `requirements.txt` : dépendances Python nécessaires au build.

`cache/` et `output/` sont des artefacts générés par Nikola. Ils ne doivent pas
être commités.

## Pré-requis locaux

- Python 3.8+
- Nikola et les dépendances du projet

Installation recommandée :

```bash
python -m pip install -r requirements.txt
```

Installation minimale :

```bash
python -m pip install nikola
```

Le plugin `github_metadata` utilise aussi `certifi`, déclaré dans
`plugins/github_metadata/requirements.txt`. Si besoin :

```bash
python -m pip install -r plugins/github_metadata/requirements.txt
```

## Commandes locales utiles

Construire le site :

```bash
nikola build
```

Prévisualiser en local :

```bash
nikola serve -b
```

Voir toutes les commandes :

```bash
nikola help
```

Nettoyer les caches avant un build propre :

```bash
nikola clean
rm -f .doit.db
```

Vérifier les liens internes après génération :

```bash
nikola check -l
```

## Thème

Le thème actif est `paradigm-shift`, configuré dans `conf.py` :

```python
THEME = "paradigm-shift"
EXTRA_THEMES_DIRS = ["."]
```

Il s'agit d'une adaptation Nikola du template HTML5 UP Paradigm Shift. Les
templates principaux sont :

- `base.tmpl` : structure globale, assets, footer et scripts ;
- `post.tmpl` : rendu standard des posts ;
- `post_gh.tmpl` : rendu du post portfolio avec liste GitHub ;
- `page.tmpl` : rendu des pages indépendantes dans la structure `<section><div class="content">`.

## Plugins locaux

Deux plugins Nikola ont été créés pour les besoins du portfolio.

### Plugin `mermaid`

Emplacement : `plugins/mermaid/`

Ce plugin ajoute un shortcode Nikola permettant d'insérer des diagrammes Mermaid
dans les contenus Markdown.

Il sont disponibles sur leur repository respectif :

- [github.com/stephmnt/shortcode_mermaid](https://github.com/stephmnt/shortcode_mermaid)
- [github.com/stephmnt/GitHub_metadata](https://github.com/stephmnt/GitHub_metadata)

Exemple d'utilisation :

```markdown
{{% mermaid %}}
mindmap
  root((Data Scientist - ML))
    Analyse de données
    MLOps
    NLP et RAG
{{% /mermaid %}}
```

Le shortcode produit un bloc HTML :

```html
<div class="mermaid">...</div>
```

Le rendu côté navigateur est assuré par le plugin lui-même : il injecte un
loader Mermaid.js protégé avec le shortcode. Le thème n'a donc pas besoin de
charger Mermaid dans `base.tmpl`.

Usage actuel : carte de compétences dans `posts/02-nouveau-depart.md`.

### Plugin `github_metadata`

Emplacement : `plugins/github_metadata/`

Ce plugin injecte un objet `github` dans le contexte global des templates Nikola,
sur le modèle de `jekyll-github-metadata`. Il permet d'afficher une liste de
dépôts GitHub sans dupliquer toute la logique dans les templates.

Configuration actuelle dans `conf.py` :

```python
GITHUB_METADATA = {
    "manual_repositories": [
        {"full_name": "stephmnt/optimisation-des-rendements-agricoles", "release_badge": True, "created_at_badge": True},
        {"full_name": "stephmnt/eval_RAGAS", "release_badge": True, "created_at_badge": True},
    ],
}
```

Le plugin peut fonctionner de deux manières :

- avec une liste manuelle de dépôts, comme dans ce projet ;
- avec l'API publique GitHub pour récupérer les dépôts publics d'un utilisateur.

Le template `post_gh.tmpl` utilise ensuite `github.public_repositories` pour
générer la liste des dépôts, les liens, les badges de release et les dates de
création.

Usage actuel : page `posts/03-portolio.md`, qui déclare :

```markdown
.. template: post_gh.tmpl
```

### Publier ou partager un plugin Nikola

Le fichier `ressources/share-plugin.md` conserve des notes sur la publication
d'un plugin dans l'index officiel Nikola. Pour un plugin partageable, les fichiers
importants sont :

- `README.md` ;
- `requirements.txt` si le plugin dépend de paquets Python ;
- `conf.py.sample` si le plugin expose des options de configuration ;
- `[plugin-name].plugin` pour les métadonnées Nikola/Yapsy ;
- `[plugin-name].py` pour le code du plugin.

## Déploiement GitHub Pages

Le déploiement est automatisé avec GitHub Actions via :

```bash
.github/workflows/deploy.yml
```

Le workflow utilise l'action `getnikola/nikola-action@v2` et exécute :

```bash
nikola github_deploy
```

Configuration attendue dans `conf.py` :

- `GITHUB_SOURCE_BRANCH = 'main'`
- `GITHUB_DEPLOY_BRANCH = 'gh-pages'`
- `GITHUB_COMMIT_SOURCE = False` car le déploiement est géré par Actions

### Configuration GitHub Pages

Dans GitHub -> Settings -> Pages :

- Source : **Deploy from a branch**
- Branch : `gh-pages` / `/(root)`

Une fois le workflow terminé, la page devient visible après quelques minutes.

### Initialiser `gh-pages` si la branche n'existe pas

```bash
git checkout --orphan gh-pages
git rm -rf .
touch .nojekyll
git commit -m "Init gh-pages"
git push origin gh-pages
git checkout main
```

## Pièges fréquents et correctifs

- `.doit.db` ne doit jamais être versionné, car son format dépend de l'OS.
  Supprimez-le localement et laissez Nikola le régénérer.
- Erreur `dbm.error: db type could not be determined` :
  supprimez `.doit.db` et relancez `nikola build`.
- `cache/` et `output/` sont des artefacts : ils ne doivent pas être commités.
- Si les badges GitHub ne s'affichent pas, vérifier la configuration
  `GITHUB_METADATA` et les champs `full_name` des dépôts.
- Si un diagramme Mermaid ne s'affiche pas, vérifier que le shortcode est bien
  fermé avec `{{% /mermaid %}}`.

## Licence du template

[HTML5 UP Paradigm Shift](https://html5up.net/paradigm-shift) est disponible
sous licence [Creative Commons BY 3.0](http://creativecommons.org/licenses/by/3.0/).
