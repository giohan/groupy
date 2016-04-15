import sys
import paramiko
from scp import SCPClient

username=''
password=''
hosts=''
verbose=False

def run_command(command, hosts):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()

    for host in hosts:
        if verbose: print('Connecting to host "%s"...' % (host))
        try:
            client.connect(host, 22, username, password)
        except paramiko.ssh_exception.AuthenticationException:
            print ('Failed to authenticate at host "%s"... Please check authentication method and username/password combination\n' % (host))
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ('Cannot connet to host %s\n' % (host))
            continue
        print ('Running "%s" at "%s"' % (command,host) if verbose else 'Host: %s'%(host))
        stdin, stdout, stderr = client.exec_command(command)
        print "stderr: ", stderr.readlines()
        print "stdout: ", stdout.readlines(),'\n'

def copy_file(script, hosts):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    for host in hosts:
        if verbose: print('Copying script "%s" to host "%s"...\n' % (script,host))
        try:
            client.connect(host, 22, username, password)
        except paramiko.ssh_exception.AuthenticationException:
            print ('Failed to authenticate at host "%s"... Please check authentication method and username/password combination\n' % (host))
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ('Cannot connet to host %s\n' % (host))
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
        if verbose: print('Connecting to host "%s"...' % (host))
        try:
            client.connect(host, 22, username, password)
        except paramiko.ssh_exception.AuthenticationException:
            print ('Failed to authenticate at host "%s"... Please check authentication method and username/password combination\n' % (host))
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ('Cannot connet to %s. Not a valid host.\n' % (host))
            continue
        print ('Running script "%s" at "%s"' % (script,host) if verbose else 'Host: %s'%(host))
        stdin, stdout, stderr = client.exec_command('chmod +x %s; sh %s; rm -f %s' %(script,script,script))
        print "stderr: ", stderr.readlines()
        print "stdout: ", stdout.readlines(), '\n'

def config(user, passwd, hostlist, verb):
    global username
    global password
    global hosts
    global verbose
    username = user
    password = passwd
    hosts = hostlist
    verbose = verb

def run(script,command,copy,user,passwd,hostlist,verb):
    config(user,passwd,hostlist,verb)

    if script == '' and command == '' and copy == '':
        print 'Please enter valid command or script to run'
        sys.exit(0)
    else:
        if verbose: print ('\nInitiating...\n')
        if command != '':
            run_command(command, hosts)
        if script != '':
            run_script(script, hosts)
        if copy != '':
            copy_file(copy, hosts)
