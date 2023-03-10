from helpers.utils.decoder import check, checkIter, decoder
from helpers.failHandler.fail import failChecker
from time import sleep
from re import sub
from helpers.clientFinder.ontType import typeCheck

existingCond = "-----------------------------------------------------------------------------"
existing = {
    "FSP": "F/S/P                   : ",
    "LP": "Line profile name    : ",
    "SRV": "Service profile name : ",
    "ONTID": "ONT-ID                  : ",
    "CF": "Control flag            : ",
    "CS": "Config state",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
    "LDT": "Last down time          : ",
    "LUT": "Last up time            : ",
    "LDGT": "Last dying gasp time    : ",
}

# improve this to return an object

def serialSearch(comm, command, data):
    command(f"display ont info by-sn {data['sn']} | no-more")
    sleep(3)
    val = decoder(comm)
    regex = checkIter(val,existingCond)
    data["fail"] = failChecker(val)
    if data["fail"] == None:
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        value = val[s:e]
        (_, eFSP) = check(value, existing["FSP"]).span()
        valFSP = value[eFSP : eFSP + 6].replace("\n", "")
        reFSP = checkIter(valFSP, "/")
        (_, eSLOT) = reFSP[0]
        (_, ePORT) = reFSP[1]
        (_, eID) = check(value, existing["ONTID"]).span()
        (_, sDESC) = check(value, existing["DESC"]).span()
        (eDESC, sLDC) = check(value, existing["LDC"]).span()
        (eLDC,_) = check(value, existing["LUT"]).span()
        (_,sLDT) = check(value, existing["LDT"]).span()
        (eLDT,_) = check(value, existing["LDGT"]).span()
        (_, sCF) = check(value, existing["CF"]).span()
        (eCF, sRE) = check(value, existing["RE"]).span()
        (eRE, _) = check(value, existing["CS"]).span()

        data["frame"]="0"
        data["slot"]= valFSP[eSLOT : eSLOT + 1].replace("\n", "")
        data["port"]= valFSP[ePORT : ePORT + 2].replace("\n", "")
        data["onu_id"]=value[eID : eID + 3].replace("\n", "")
        data["name"]=sub(" +", " ", value[sDESC:eDESC]).replace("\n", "")
        data["control_flag"]=value[sCF:eCF].replace("\n", "")
        data["run_state"]=value[sRE:eRE]
        data["device"]=None
        data["last_down_cause"]=value[sLDC:eLDC].replace("\n", "").replace("\r", "")
        data["last_down_date"]=value[sLDT:eLDT][:10].replace("\n", "").replace("\r", "")
        data["last_down_time"]=value[sLDT:eLDT][11:].replace("\n", "").replace("\r", "")
        data["device"] = typeCheck(comm,command,data)
    
    return data
