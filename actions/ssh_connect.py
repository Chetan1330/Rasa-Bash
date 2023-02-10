# from paramiko import SSHClient

# client = SSHClient()
# # client.load_system_host_keys()
# # client.load_host_keys('~/.ssh/known_hosts')
# # client.set_missing_host_key_policy(AutoAddPolicy())

# client.connect('192.168.0.106', username='bitthal', password='ladiwal0909')
# client.exec_command('ls')
# client.close()

# import asyncssh
# import asyncio
# import getpass
# async def execute_command(host, command = 'ls', username = 'bitthal', password = 'ladiwal0909'):
#     async with asyncssh.connect(host, username = username, password= password) as connection:
#         connection



import paramiko
import sys
import asyncio, asyncssh, sys

def ssh_exec_command(host, username, password, command):
    results = []
    client = paramiko.SSHClient()
    proxy = None
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, sock=proxy)
    ssh_stdin, ssh_stdout, shh_stderr = client.exec_command(command)
    # for line in ssh_stdout:
    #     results.append(line.strip('\n'))
    # return '\n'.join([item for item in results])
    return ssh_stdout.read().decode('utf-8')


def ssh_conn_check(host, username, password, command):
    try:
        client = paramiko.SSHClient()
        proxy = None
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, sock=proxy)
        ssh_stdin, ssh_stdout, shh_stderr = client.exec_command(command)
        return True
    except Exception as e:
        print(e)
        return False


# async def run_client(host, username, password, command):
#     try:
#         async with asyncssh.connect(host = host, username = username, password= password, known_hosts=None) as conn:
#             result = await conn.run(command, check=True)
#             return result.stdout
#     except Exception as e:
#         return "Error occured: " + e