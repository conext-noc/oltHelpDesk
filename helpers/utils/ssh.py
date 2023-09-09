from time import sleep
import paramiko
from helpers.utils.printer import log
from helpers.utils.request import db_request
from helpers.info.definitions import endpoints


def ssh(ip):
    count = 1
    delay = 0.85
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    comm = None
    cont = True
    creds = db_request(endpoints["get_creds"], {})

    # Handling multiple SSH sessions
    while cont and count <= 3:
        try:
            username = creds["data"][count]["user_name"]
            password = creds["data"][count]["password"]
            port = 22
            conn.connect(ip, port, username, password)
            comm = conn.invoke_shell()
            cont = False
        except paramiko.ssh_exception.AuthenticationException:
            cont = True
            count += 1
            continue
        break

    def enter():
        comm.send(" \n")
        comm.send(" \n")
        sleep(delay)

    def command(cmd):
        comm.send(cmd)
        sleep(delay)
        enter()

    def quit_ssh():
        conn.close()

    if ip in ["181.232.180.5", "181.232.180.6", "181.232.180.7"]:
        command("enable")
        command("config")
        command("scroll 512")
    else:
        command("sys")

    return (comm, command, quit_ssh)
