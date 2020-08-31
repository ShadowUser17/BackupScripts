#!/usr/bin/env python3
from traceback import print_exc
import subprocess as sp
#
#
snmp_community = 'write'
tftp_server = ''
tftp_devdb = 'devdb.txt'
#
mib_tftp_address = ('1.3.6.1.4.1.45.1.6.4.4.5.0', 'a')
mib_tftp_file = ('1.3.6.1.4.1.45.1.6.4.4.6.0', 's')
mib_tftp_upload = ('1.3.6.1.4.1.45.1.6.4.4.19.0', 'i', '4')
#
#
def read_dev_list(fname):
    items = None
    with open(fname) as devdb:
        items = map(str.split, devdb)
        items = filter(None, items)
        items = map(tuple, items)
        items = list(items)
    #
    return items
#
#
def send_snmp(ip, mib, type, value, community):
    cmd = 'snmpset -v2c -c {comm} {ip} {mib} {type} {value}'.format(
        comm=community, ip=ip, mib=mib, type=type, value=value
    )
    snmp = sp.Popen(cmd, stdout=sp.DEVNULL, stderr=sp.PIPE, shell=True)
    output = snmp.communicate()
    #
    output = output[1]
    return (snmp.args, output.decode())
#
#
def snmp_send(ip, file):
    # Set TFTP server ip.
    (mib, type) = mib_tftp_address
    (cmd, res) = send_snmp(ip, mib, type, tftp_server, snmp_community)
    print('CMD: {}'.format(cmd), 'OUT: {}'.format(res), sep='\n')
    #
    # Set file name.
    (mib, type) = mib_tftp_file
    (cmd, res) = send_snmp(ip, mib, type, file, snmp_community)
    print('CMD: {}'.format(cmd), 'OUT: {}'.format(res), sep='\n')
    #
    # Start upload.
    (mib, type, value) = mib_tftp_upload
    (cmd, res) = send_snmp(ip, mib, type, value, snmp_community)
    print('CMD: {}'.format(cmd), 'OUT: {}'.format(res), sep='\n')
#
#
def main():
    try:
        if not tftp_server: raise ValueError('Variable is empty!')
        #
        dev_list = read_dev_list(tftp_devdb)
        for (ip, file) in dev_list: snmp_send(ip, file)
        #
    except Exception: print_exc()
#
#
if __name__ == '__main__': main()
