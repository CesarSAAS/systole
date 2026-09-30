# Crédits et licences des éléments tiers

## Modèles anatomiques 3D

Fichiers concernés : `models/m_coeur.json`, `models/m_squelette.json`, `models/m_tronc.json`.

| Source | Licence |
| --- | --- |
| BodyParts3D, © The Database Center for Life Science (DBCLS) : la géométrie de base | [CC BY-SA 2.1 Japan](https://creativecommons.org/licenses/by-sa/2.1/jp/) |
| [Z-Anatomy](https://www.z-anatomy.com/) : la version retravaillée, nommée et regroupée | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

Les maillages ont été extraits des fichiers exportés par le projet [nqwrc/3d-anatomy](https://github.com/nqwrc/3d-anatomy), puis modifiés pour Systole : sélection de structures, fusion par structure, réduction du nombre de triangles, quantification des coordonnées, couleurs.

Ces trois fichiers sont donc des œuvres dérivées. Ils sont mis à disposition sous **CC BY-SA 4.0**, avec les attributions ci-dessus. Cette licence autorise l'usage commercial, à condition de créditer les sources et de partager les versions modifiées des modèles sous la même licence.

### À vérifier avant un usage commercial

Le projet nqwrc/3d-anatomy est distribué dans son ensemble sous CC BY-NC-SA 4.0 (non commercial), parce que deux de ses composants le sont : le rein (fichier `visceral.glb`, CC BY-NC 4.0) et l'oreille interne (fichier `nervous.glb`, CC BY-NC-SA 4.0). Sa licence précise que tout le reste vient de sources autorisant l'usage commercial.

Ce qui a été fait ici :

- le rein n'est pas dans `m_tronc.json` ;
- `nervous.glb` n'a pas été utilisé, donc ni l'oreille interne ni les maillages du cerveau, dont la licence n'est pas indiquée par leur source ;
- les fichiers `.glb` d'origine ne sont pas dans ce dépôt.

Ceci n'est pas un avis juridique. Avant une version payante, deux précautions : faire valider cette lecture, et de préférence régénérer les trois modèles directement depuis le fichier Blender de Z-Anatomy (CC BY-SA 4.0), pour ne plus dépendre d'un intermédiaire.

## Molécules

Fichiers concernés : `models/m_adn.json`, `models/m_hemoglobine.json`, `tools/models/1BNA.pdb`, `tools/models/2HHB.pdb`.

Structures issues de la [RCSB Protein Data Bank](https://www.rcsb.org/), dont les données sont dans le domaine public (CC0 1.0) :

- ADN : [PDB 1BNA](https://www.rcsb.org/structure/1BNA), Drew et al., 1981 ;
- Hémoglobine : [PDB 2HHB](https://www.rcsb.org/structure/2HHB), Fermi et al., 1984.

## Cellule, schémas, mascotte, sons

La cellule 3D, les schémas (ECG, neurone, chromosome, cellule 2D), la mascotte Boum, les icônes et les sons ont été créés pour Systole. Les sons sont fabriqués par le navigateur : il n'y a aucun fichier audio.

## Logiciels et polices

| Élément | Licence |
| --- | --- |
| [three.js](https://threejs.org/) r128, chargé depuis cdnjs | MIT |
| Polices Baloo 2, Nunito et Caveat, chargées depuis Google Fonts | SIL Open Font License 1.1 |
| Outils de la chaîne 3D : DracoPy, pyfqmr, NumPy | voir chaque projet |
