# Chaîne de fabrication des modèles 3D

Ce dossier sert à refabriquer les fichiers de `models/`. L'app n'en a pas besoin pour fonctionner.

## Ce qu'il faut

```bash
pip install numpy DracoPy pyfqmr
```

## Molécules (ADN, hémoglobine)

Les deux fichiers `.pdb` sont fournis.

```bash
cd tools/models
python3 build_mol.py
mv m_adn.json m_hemoglobine.json ../../models/
```

L'ADN est redressé pour que l'axe de l'hélice soit vertical. Les groupes hème sont dessinés 1,3 fois plus gros pour rester trouvables.

## Anatomie (cœur, squelette, tronc)

Les fichiers sources ne sont pas dans le dépôt. Il faut placer dans ce dossier `cardiovascular.glb`, `skeletal.glb` et `visceral.glb`, exportés depuis Z-Anatomy. Voir `CREDITS.md` pour les licences : `visceral.glb` contient un rein sous licence non commerciale, qui n'est pas repris.

```bash
cd tools/models
python3 build_models.py coeur
python3 build_models.py squelette
python3 build_models.py tronc
mv m_coeur.json m_squelette.json m_tronc.json ../../models/
```

`specs.json` décide de tout : quelles structures sont gardées, sous quel nom et quelle couleur, et combien de triangles chaque modèle a le droit d'utiliser.

Ce que fait `build_models.py` pour chaque structure : décompresser le maillage (Draco), fusionner les sommets en double, réduire le nombre de triangles, puis enregistrer les coordonnées sur 16 bits.

| Fichier | Rôle |
| --- | --- |
| `glbx.py` | lit un fichier `.glb` et ses maillages compressés |
| `glbinfo.py`, `listparts.py` | listent les structures d'un `.glb`, pour remplir `specs.json` |
| `build_models.py` | fabrique un modèle d'anatomie |
| `build_mol.py` | fabrique les deux molécules |

Si le nom ou la liste des structures change, mettre à jour `src/parts.json`, puis relancer `python3 tools/build.py`.
