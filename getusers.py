#!/usr/bin/env python
import argparse
import commands
import json
import time

class ASAVpn():
    def __init__(self, firewall, ignore_list, community_string):
        self.firewall = firewall
        self.ignore_list = ignore_list
        self.cmd = 'snmpwalk -v1 -c%s %s 1.3.6.1.4.1.9.9.392.1.3.21.1.10' % (community_string, firewall)

    def get_connected_users(self):
        output = commands.getoutput(self.cmd)
        output = self._commands_output_to_list(output)
        output = self._get_ascii_codes(output)
        output = self._ascii_string_to_int(output)
        output = self._convert_ascii_code_to_text(output)
        output = self._strip_ip_element(output)
        output = self._remove_ignore_list(output)
        output = self._convert_to_json(output)
        return output


    def _commands_output_to_list(self, output):
        """Take snmpwalk command output and turn it to a list
        based on \n and =  so format [[oid, result]]"""
        return [x.split('=') for x in output.split('\n')]


    def _get_ascii_codes(self, output):
        """Strip SNMP stuff from the oid, including whitespace
        and the first and last element of the list. This give us a
        list like this: ['105 97 110', ' STRING: "31.23.24.56"'] """
        string_to_remove = 'SNMPv2-SMI::enterprises.9.9.392.1.3.21.1.10.'
        output = [[x[0].replace(string_to_remove,'').strip(' '), x[1]] for x in output]
        output = [[' '.join(x[0].split('.')[1:-1]), x[1]] for x in output]
        return output


    def _ascii_string_to_int(self, output):
        """turn the first element of ['105 97 110', ' STRING: "31.23.24.56"']
        into a list of integers: [[105 97 110], ' STRING: "31.23.24.56"']"""
        new = list()
        for x in output:
            split = x[0].split()
            to_int = [int(y) for y in split]
            new.append([to_int, x[1]])
        return new


    def _convert_ascii_code_to_text(self, output):
        """Now lets convert our ascii codes to a text name
        and return a new list object ['username': ' STRING: "31.23.24.56"']"""
        new = list()
        for x in output:
            username_as_ascii = x[0]
            username_as_text = ''.join(chr(i) for i in username_as_ascii)
            new.append([username_as_text, x[1]])
        return new


    def _strip_ip_element(self, output):
        """Clean up the second element and remove extraneous " and 
        ' STRING: '"""
        return [[x[0], x[1].strip(' STRING: ').replace('"','')] for x in output]


    def _remove_ignore_list(self, output):
        """return us only VPN users and not the ignore list"""
        new = list()
        for x in output:
            if not x[0] in self.ignore_list:
                new.append(x)
        return new


    def _convert_to_json(self, output):
        out = {'users' : dict()}
        for i in output:
            out['users'].update({i[0]:{'Public IP':i[1]}})
        return out


def parse_args():
    parser = argparse.ArgumentParser(description='Get connected users from ASA via SNMP')
    parser.add_argument('-f', '--firewall', action='store', required=True, help='Address of the Cisco ASA')
    parser.add_argument('-i', '--ignore', action='store', default='', help='Comma separated list of IP addresses to ignore')
    parser.add_argument('-c', '--community_string', action='store', required=True, help='SNMP community string')
    parser.add_argument('-o', '--output', action='store', default='json', help='Output type, option are json and text. Defaults to json')
    return parser.parse_args()

args = parse_args()


def main():
    asa = ASAVpn(args.firewall, args.ignore, args.community_string)
    users = asa.get_connected_users()
    if args.output == 'text':
        for i in users['users']:
            print ('%s, %s' % (i, users['users'][i]['Public IP']))
    else:
        print users


if __name__ == "__main__":
    main()
