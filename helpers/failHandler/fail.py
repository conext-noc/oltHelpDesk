from helpers.utils.decoder import check, checkIter
from helpers.utils.printer import colorFormatter

FAIL_1 = "Failure: "
FAIL_1_CHAR = "% "
END_FAIL = "MARLLM0"
FAIL_2 = "The required ONT does not exist"
FAIL_3 = "WAN port does not exist"


def failChecker(value):
    fail1 = check(value, FAIL_1)
    fail2 = check(value, FAIL_1_CHAR)
    fail3 = check(value, FAIL_2)
    fail4 = check(value, FAIL_3)
    if fail1 == None and fail2 == None and fail3 == None and fail4 == None:
        return None
    elif fail1 != None and fail2 == None and fail3 == None and fail4 == None:
        (_, s) = fail1.span()
        end = checkIter(value, END_FAIL)
        maxLen = len(end) - 1
        (e, _) = end[maxLen]
        reason = value[s:e].replace("\n", "")
        # reason = colorFormatter(reason, "fail")
        reason = colorFormatter(f"""
LA ACCION FALLO POR LA SIGUENTE RAZON: {reason}

CONTACTAR AL NOC PARA MAS INFORMACION
""", "fail")
        return reason
    elif fail1 == None and fail2 != None and fail3 == None and fail4 == None:
        (_, s) = fail2.span()
        end = checkIter(value, END_FAIL)
        maxLen = len(end) - 1
        (e, _) = end[maxLen]
        reason = value[s:e].replace("\n", "")
        # reason = colorFormatter(reason, "fail")
        reason = colorFormatter("""
PROBLEMA DE COMMANDOS

CONTACTAR AL NOC EN CASO DE PERSISTIR ESTE PROBLEMA""", "fail")
        return reason
    elif fail1 == None and fail2 == None and fail3 != None and fail4 == None:
        # reason = colorFormatter(FAIL_2, "fail")
        reason = colorFormatter("EL ONT NO EXISTE EN ESTA OLT", "fail")
        return reason
    elif fail1 == None and fail2 == None and fail3 == None and fail4 != None:
        # reason = colorFormatter(FAIL_3, "fail")
        reason = colorFormatter("EL CLIENTE HIZO RESET, O ESTE ONT ES UN BRIDGE", "fail")
        return reason
