# Systole

Le Duolingo de la médecine pour les lycéens : 5 minutes par jour pour arriver en études de santé avec une longueur d'avance.

Des leçons courtes, des questions, une série de jours (les « battements »), des cœurs, des gélules à dépenser, des coffres, et un Labo 3D où l'on touche de vrais modèles anatomiques. La mascotte s'appelle Boum.

**État actuel : prototype.** La progression est enregistrée dans le navigateur de chaque personne. Il n'y a ni compte, ni serveur, ni paiement.

## Lancer l'app sur son ordinateur

Il faut seulement Python 3, déjà présent sur macOS.

```bash
python3 -m http.server 8000
```

Puis ouvrir <http://localhost:8000>. Ouvrir `index.html` par double-clic ne suffit pas : les modèles 3D ne se chargent que depuis un serveur.

## Modifier l'app

| Pour changer… | Fichier |
| --- | --- |
| Les cours et les questions | `src/programme.json` |
| L'interface, les animations, la mascotte | `src/app.html` |
| Le nom des structures 3D | `src/parts.json` |

Après une modification, reconstruire la page :

```bash
python3 tools/build.py
```

Cela réécrit `index.html` (la page complète, celle qui est mise en ligne) et `dist/artifact.html` (la même app, au format d'un artifact Claude).

## Contenu du dépôt

```
index.html        la page construite, prête à être hébergée
models/           les 5 modèles 3D chargés par l'app
src/              les sources de l'app et le contenu des cours
tools/build.py    assemble src/ en index.html
tools/models/     la chaîne qui a produit models/ à partir des sources publiques
CREDITS.md        sources et licences des éléments tiers
```

Le contenu des cours : 10 matières, 99 leçons. Chaque leçon a 2 diapos, un récap, 4 paires à relier et 4 ou 5 questions. 20 leçons ont une question où il faut toucher une structure sur un modèle 3D ou un schéma.

## Mettre en ligne

C'est un site statique : n'importe quel hébergeur convient (GitHub Pages, Vercel, Netlify). Il faut publier `index.html` et le dossier `models/` au même endroit.

Le moteur 3D (three.js) et les polices sont chargés depuis des serveurs publics au moment de l'utilisation.

## Avant une version payante

- Des comptes et une progression enregistrée côté serveur.
- Un paiement.
- Une relecture des cours par un enseignant ou un étudiant avancé.
- Le cadre légal pour un public mineur : CGU, politique de confidentialité, accord parental pour les moins de 15 ans.
- La vérification des licences des modèles 3D : voir `CREDITS.md`.

## Droits

Le code, les textes des cours et la mascotte : © 2026 Systole, tous droits réservés.
Les éléments tiers gardent leur propre licence : voir `CREDITS.md`.
