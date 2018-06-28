#!/usr/bin/env python

import argparse
import logging

FORMAT = '%(asctime)20s:%(module)15s:%(funcName)20s:%(lineno)4s - %(levelname)7s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('smartLicensingConfigurator')
logger.setLevel(logging.DEBUG)
try:
    import cli
except Exception as e:
    logger.warning("failed to import cli module")

def configure_smart_licensing(idtoken, throughput):
    if idtoken is None:
        logger.warning("idtoken value is None. Please provide valid idtoken")
        return False

    email='sch-smart-licensing@cisco.com'
    smart_licensing_configuration = '''
    service call-home
    call-home
    contact-email-addr {}
    profile "CiscoTAC-1"
    active
    destination transport-method http
    no destination transport-method email
    destination address http https://tools.cisco.com/its/service/oddce/services/DDCEService
    
    license smart enable
    do license smart register idtoken {}
    platform hardware throughput level MB {}
    '''.format(idtoken, throughput, email)
    logger.info("Trying to configure smart licensing. Configs: {}".format(smart_licensing_configuration))
    cli.configure(smart_licensing_configuration)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to Configure Smart licensing on CSR")
    parser.add_argument('--idtoken', action='store', dest='idtoken', type=str,
                        help='provide account idtoken string')
    parser.add_argument('--throughtput', help='provide desired throughtput level in MB. default is 2500',
                        action='store', type=str,
                        dest='throughput', default='2500')
    args = parser.parse_args()
    logger.info("idtoken: {}".format(args.idtoken))
    logger.info("throughput: {}".format(args.throughput))
    configure_smart_licensing(args.idtoken, args.idtoken)