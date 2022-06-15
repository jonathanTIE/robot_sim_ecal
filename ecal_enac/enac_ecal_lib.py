import ecal.core.core as ecal_core

#TODO : faire une fonction qui trouve les fichiers protobuf python a importer en tant que modulez

#log 3 doesn't work, I can"t find fatal and debug options in real python API (not the documentation)
def log_info(msg:str):
    ecal_core.log_setlevel(1) #INFO
    ecal_core.log_message(msg)
    ecal_core.log_setlevel(1) #reset to 0 by default

def log_warn(msg:str):
    ecal_core.log_setlevel(2) #warn
    ecal_core.log_message(msg)
    ecal_core.log_setlevel(1) #reset to 0 by default

def log_error(msg:str):
    ecal_core.log_setlevel(4) #''fatal'' 
    ecal_core.log_message(msg)
    ecal_core.log_setlevel(1) #reset to 0 by default
    
