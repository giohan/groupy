import sys
import paramiko
from scp import SCPClient

username=''
password=''
hosts=''

def run_command(command, hosts):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()

    for host in hosts:
        print('\nConnecting to host "%s"...' % (host))
        try:
            client.connect(host, 22, username, password)
        except paramiko.ssh_exception.AuthenticationException:
            print ('Failed to authenticate at host "%s"... Please check authentication method and username/password combination' % (host))
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ('Cannot connet to host %s' % (host))
            continue
        print ('Running "%s" at "%s"' % (command,host))
        stdin, stdout, stderr = client.exec_command(command)
        print "stderr: ", stderr.readlines()
        print "stdout: ", stdout.readlines()
        print 'Done %s' %(host)

def copy_file(script, hosts):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    for host in hosts:
        print('\nCopying script "%s" to host "%s"...' % (script,host))
        try:
            client.connect(host, 22, username, password)
        except paramiko.ssh_exception.AuthenticationException:
            print ('Failed to authenticate at host "%s"... Please check authentication method and username/password combination' % (host))
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ('Cannot connet to host %s' % (host))
            continue

        scp = SCPClient(client.get_transport())

        scp.put(script, script)

        scp.close()


def run_script(script, hosts):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()

    copy_file(script, hosts)

    for host in hosts:
        print('\nConnecting to host "%s"...' % (host))
        try:
            client.connect(host, 22, username, password)
        except paramiko.ssh_exception.AuthenticationException:
            print ('Failed to authenticate at host "%s"... Please check authentication method and username/password combination' % (host))
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ('Cannot connet to %s. Not a valid host.' % (host))
            continue
        print ('Running script "%s" at "%s"' % (script,host))
        stdin, stdout, stderr = client.exec_command('chmod +x %s; ./%s; rm -f %s' %(script,script,script))
        print "stderr: ", stderr.readlines()
        print "stdout: ", stdout.readlines()

def config(user, passwd, hostlist):
    global username
    global password
    global hosts
    username = user
    password = passwd
    hosts = hostlist

def run(script,command,copy,user,passwd,hostlist):
    config(user,passwd,hostlist)

    if script == '' and command == '' and copy == '':
        print 'Please enter valid command or script to run'
        sys.exit(0)
    else:
        if command != '':
            run_command(command, hosts)
        if script != '':
            run_script(script, hosts)
        if copy != '':
            copy_file(copy, hosts)