# RobotSim

A simple robot simulator, to be used by students as test bench for a programming project.

It should be used with eCAL(5.10).

# Installation

Install Python binding for eCAL
    https://eclipse-ecal.github.io/ecal/_download_archive/download_archive_ecal_5_10_1.html#download-archive-ecal-v5-10-1

# Usage

Just execute `robot_sim.py` in `robot_sim_ecal` to launch the simulator

For basic console control (forward, backward,... ), execute `dyn_pub.py` in `ecal_enac/experiments`
 
## Compilation des fichiers de définition

En cas de modification des fichiers de définition des messages protobuf, il est nécessaire de les reconpiler pour que ça soit pris en compte.
Une fois protobuf installé, on peut exécuter soit :

#### Dans le répertoire racine (du readme):

    (Jonathan : Problème de compilation sous windows, le python_out ne marche pas dans le dossier documents, il faut output autre part)

    protoc -I="./proto" --python_out="proto/py" proto/*

#### Dans le dossier proto


    protoc -I="." --python_out="py" *

### Développement 

#### Installation d'un environement virtuel python

1. dans le répertoire racine ecal_test_2022, python -m venv .venv

2. activer l'environnement (sur vscode, select interpreter ou avec l'extension python l'activer) [TODO à détailller]

3. installer le requirements dedans
#### TODO 

Dans le requirements.txt, installer les proto & les ecal_lib custom
(Refactoriser pour n'avoir qu'un fichierpour les pb2 en tant que module et pas le mettre dans tous les dossiers)
Vérifier les arrondis en conversion python -> protobuf-> Python

#### Requirements.txt

Attention, il n'est pas à jour, il a été généré automatiquement