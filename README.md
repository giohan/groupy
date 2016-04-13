# Groupy

Groupy is a really simple tool to help you with multinode orchestration.

# Features

Groupy can be used in order to:  
- Run single commands  
- Run scripts  
- Copy files  
on multiple nodes

## Concepts
**Leader**: Is the machine which is used to run groupy.  
**Followers**: Are the nodes we are sending the commands to.  
**Groups**: We can send commands to groups of Followers(nodes) using the **hosts** file  

# Dependancies

Groupy can manage clusters from a single machine (i.e. just your laptop) with no dependancies on Follower nodes.
You don't even need to install groupy on multiple nodes.

The only dependancies are * *paramiko* * and * *scp* *on the Leader node and ssh access to the Follower nodes.
```
sudo pip install paramiko
sudo pip install scp
```

# Usage
```
usage: groupy [-h] [-H HOSTS] [-g GROUPS] [-u USER] [-p] [-s SCRIPT]
              [-c COMMAND] [-C COPY]

Script to help you manage clusters easily

optional arguments:
  -h, --help                    show this help message and exit
  -H HOSTS, --hosts HOSTS       Follower Hosts
  -g GROUPS, --groups GROUPS    Follower Groups
  -u USER, --user USER          Username
  -p, --password                Is password required. Do not enter password here.
  -s SCRIPT, --script SCRIPT    Script to run
  -c COMMAND, --command COMMAND Shell command to run
  -C COPY, --copy COPY          File to copy
```
- Only one between **hosts** and **groups** options can be used at each time.
- Both **hosts** and **groups** accept a comma separated list as input. The **all** keyword can be used for groups, in order to run the command for all hosts in all groups.
- If you use the **password** flag, you will be promted to enter the password, in order to not expose it in plain text.
- You can use multiple operations(script,command,copy) in a single run.
- Multiple commands can be run in the format:
> -c 'command-1; command-2'
- When running a script, it is copied in the home directory in all nodes and after running it is removed.