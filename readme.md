
## Compilation des fichiers de définition

En cas de modification des fichiers de définition des messages protobuf, il est nécessaire de les reconpiler pour que ça soit pris en compte.
Une fois protobuf installé, on peut exécuter soit :

#### Dans le répertoire racine (du readme):

    protoc -I="./proto" --python_out="proto/py" proto/*

#### Dans le dossier proto

    
    protoc -I="." --python_out="py" *

