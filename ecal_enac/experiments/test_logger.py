from ensurepip import version
import sys
import time
import ecal.core.core as ecal_core
from ecal_enac.enac_ecal_lib import log_error, log_info, log_warn

ecal_core.initialize(sys.argv, "test")

while ecal_core.ok():
    log_error("test erreur")
    log_info("info ")
    log_info("  ")
    log_info("")
    time.sleep(0.5)
  # finalize eCAL API
ecal_core.finalize()
#ecal_core.log_setlevel