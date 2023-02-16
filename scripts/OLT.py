from helpers.info.hashMaps import devices
from helpers.utils.decoder import decoder
from helpers.utils.printer import inp, log, colorFormatter
from helpers.utils.ssh import ssh
from time import sleep
from scripts.BC import existingLookup
from scripts.VC import verifyTraffic
from scripts.XP import portOperation


def olt():
    """    
    This module handles all olt requests
    """
    oltOptions = ["1", "2", "3"]
    olt = inp("Seleccione la OLT [1 | 2 | 3] (1: X15 Nueva, 2: X15 Vieja, 3: X2): ").upper()
    if olt in oltOptions:
        ip = devices[f"OLT{olt}"]
        (comm, command, quit) = ssh(ip)
        decoder(comm)

        action = inp(
            """
Que accion se realizara? 
    > (BC)  :   Buscar cliente en OLT
    > (VC)  :   Verificar consumo
    > (VP)  :   Verificacion de puerto
    > (CA)  :   Clientes con averias (corte de fibra)
$ """
        )

        modules = {
            "BC": existingLookup,
            "VC": verifyTraffic,
            "VP": portOperation,
            "CA": portOperation,
        }

        modules[action](comm, command, quit, olt, action)
    else:
        resp = colorFormatter(
            f"No se puede Conectar a la OLT, Error OLT {olt} no existe", "warning")
        log(resp)
        sleep(1)
