#!/usr/bin/env python3
import logging
import pif

from pygodaddy import GoDaddyAccount
from accounts import accounts

def init(log_file):
    init_logger(log_file)

def init_logger(log_file):
    logging.basicConfig(filename=log_file,
                format='%(asctime)s %(message)s',
                level=logging.INFO)

def get_public_ip():
    return pif.get_public_ip()

def get_cached_ip(fname):
    content = None
    try:
        with open(fname, 'r') as content_file:
            content = content_file.read().strip()
    except FileNotFoundError as e:
        logging.warning(e)
    finally:
        return content

def update_cached_ip(fname, new_ip):
    logging.debug('Updating cached ip ...')
    try:
        with open(fname, 'w') as content_file:
            content_file.write(new_ip)
            logging.info('Cached ip is updated to {0}'.format(new_ip))
    except Exception as e:
        logging.error('Failed. Error = {0}'.format(e))

def update_godaddy_dns_for_single_user_multi_domain(
    public_ip, username, password, domain_white_list):
    logging.debug('For user {0}, updating dns record for domains {1}'.format(
        username, domain_white_list))
    try:
        with GoDaddyAccount(username, password) as client:
            if not client:
                logging.error('Login failed. user="{0}"'.format(username))
                return False
            for domain in client.find_domains():
                if domain_white_list and (domain not in domain_white_list):
                    logging.warning('Skipped "{0}"'.format(domain))
                else:
                    dns_records = list(client.find_dns_records(domain))
                    logging.info("Domain '{0}' DNS records: {1}".format(
                        domain, dns_records))
                    client.update_dns_record(domain, public_ip)
                    logging.info("Domain '{0}' public IP set to '{1}'".format(
                        domain, public_ip))
    except Exception as e:
        logging.error('Failed. Error = {0}'.format(e))
        return False
    return True

def update_godaddy_dns(accounts, public_ip):
    logging.debug('Updating Godaddy dns record ...')
    for _, account in enumerate(accounts):
        if not update_godaddy_dns_for_single_user_multi_domain(
                        public_ip,
                        account['username'],
                        account['password'],
                        account['domains']):
            return False
    return True

def godaddy_ddns():
    CACHED_IP_FILE = 'cached_ip'
    LOG_FILE = 'godaddy-dyndns.log'
    init(log_file=LOG_FILE)
    logging.info('######## Godaddy DDNS update utility init ...')
    old_ip = get_cached_ip(CACHED_IP_FILE) # Previously updated to godaddy
    new_ip = get_public_ip()
    if old_ip == new_ip:
        logging.info('IP has not changed since last update. Nothing to do.')
    else:
        logging.info('IP has been changed from "{0}" to "{1}"'.format(
            old_ip, new_ip))
        if update_godaddy_dns(accounts, new_ip):
            update_cached_ip(CACHED_IP_FILE, new_ip)

def main():
    godaddy_ddns()

if __name__ == '__main__':
    main()
