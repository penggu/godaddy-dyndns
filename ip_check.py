#!/usr/bin/env python3
import socket

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

def test():
    addresses = [
        '12.3.2.3',
        'False',
        '255.255.255.255',
        '12.3.2.a',
        '12.3.2.00003',
        '12.3.2',
        '12.3.2.1.1',
        '12.3.2.0x3',
        '12.3.2.b1111',
        '12.3.2.3abc'
        ]
    for addr in addresses:
        print('"{0}" {1} a valid IPv4 address.'.format(addr, is_valid_ipv4_address(addr) and 'is' or 'is not'))

def main():
    test()

if __name__ == '__main__':
    main()
