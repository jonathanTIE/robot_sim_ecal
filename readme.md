# RobotSim

A simple robot simulator, to be used by students as test bench for a programming project.

It should be used with eCAL(5.10).


# Usage

Just execute `robot_sim.py` in `robot_sim_ecal` to launch the simulator

For basic console control (forward, backward,... ), execute `dyn_pub.py` in `ecal_enac/experiments`
 
## Compilation des fichiers de définition

En cas de modification des fichiers de définition des messages protobuf, il est nécessaire de les reconpiler pour que ça soit pris en compte.
Une fois protobuf installé, on peut exécuter soit :

#### Dans le répertoire racine (du readme):

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

#### Requirements.txt

Attention, il n'est pas à jour, il a été généré automatiquement