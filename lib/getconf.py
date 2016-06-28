import getpass
import sys
import ConfigParser


def get_groups(sections):
    Config = ConfigParser.ConfigParser(allow_no_value=True)

    Config.read('../conf/hosts')
    hosts = []
    if sections == 'all':
        sections = Config.sections()
    else:
        sections = sections.split(',')

    for section in sections:
        for key in Config.items(section):
            if key[0][0] == '$':
                sections.append(key[0][1:])
                continue
            if key[0] not in hosts:
                hosts.append(key[0])

    return hosts

def get(args):
    if args['password']:
        args['password'] = getpass.getpass()

    if args['hosts'] != 'localhost' and args['groups'] != '':
        print 'Exactly one option between "hosts" and "groups" must be used'
        sys.exit(0)
    elif args['groups'] != '':
        args['hosts'] = get_groups(args['groups'])
    else:
        args['hosts'] = args['hosts'].split(',')

    return args
