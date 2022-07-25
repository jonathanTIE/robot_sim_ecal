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