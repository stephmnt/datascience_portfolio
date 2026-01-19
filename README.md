# Datascience Portfolio (Nikola)

Ce dépôt contient le code source du site statique généré avec Nikola.

Documentation officielle : https://getnikola.com/
Fichier de configuration : `conf.py`

## Pré-requis locaux

- Python 3.8+
- Nikola (`pip install nikola`)

## Commandes locales utiles

Construire le site :
```
nikola build
```

Prévisualiser en local :
```
nikola serve -b
```

Voir toutes les commandes :
```
nikola help
```

Nettoyer les caches (utile avant un build propre) :
```
nikola clean
rm -f .doit.db
```

## Déploiement GitHub Pages (workflow)

Le déploiement est automatisé avec GitHub Actions via :
```
.github/workflows/deploy.yml
```

Le workflow utilise l’action `getnikola/nikola-action@v2` et exécute :
```
nikola github_deploy
```

Configuration attendue dans `conf.py` :
- `GITHUB_SOURCE_BRANCH = 'main'`
- `GITHUB_DEPLOY_BRANCH = 'gh-pages'`
- `GITHUB_COMMIT_SOURCE = False` (car le déploiement est géré par Actions)

### Configuration GitHub Pages

Dans GitHub → Settings → Pages :
- Source : **Deploy from a branch**
- Branch : `gh-pages` / `/(root)`

Une fois le workflow terminé, la page devient visible après quelques minutes.

### Initialiser `gh-pages` (si la branche n’existe pas)

```
git checkout --orphan gh-pages
git rm -rf .
touch .nojekyll
git commit -m "Init gh-pages"
git push origin gh-pages
git checkout main
```

## Pièges fréquents et correctifs

- `.doit.db` ne doit jamais être versionné (format dépendant de l’OS).
  Supprimez-le localement et laissez Nikola le régénérer.
- Erreur `dbm.error: db type could not be determined` :
  supprimez `.doit.db` et relancez un `nikola build`.
- `cache/` et `output/` sont des artefacts : ils ne doivent pas être commités.
