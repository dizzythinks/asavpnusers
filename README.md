This should work with stqandard Python libraries. You will need to enable SNMP on the Cisco ASA

USAGE
=====

        usage: asausers.py [-h] -f FIREWALL [-i IGNORE] -c COMMUNITY_STRING
                           [-o OUTPUT]

        Get connected users from ASA via SNMP

        optional arguments:
          -h, --help            show this help message and exit
          -f FIREWALL, --firewall FIREWALL
                                Address of the Cisco ASA
          -i IGNORE, --ignore IGNORE
                                Comma separated list of IP addresses to ignore
          -c COMMUNITY_STRING, --community_string COMMUNITY_STRING
                                SNMP community string
          -o OUTPUT, --output OUTPUT
                                Output type, option are json and text. Defaults to json'


OUTPUTS
========

        {'users': {'bob.jones': {'Public IP': '1.2.3.4'}, 'dave.jones': {'Public IP': '1.2.3.5'}}}


        bob.jones, 1.2.3.4
        dave.jones, 1.2.3.4
