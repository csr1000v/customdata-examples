#!/usr/bin/env python

import argparse
import logging
import time
FORMAT = '%(asctime)20s:%(module)15s:%(funcName)20s:%(lineno)4s - %(levelname)7s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('smartLicensingConfigurator')
logger.setLevel(logging.DEBUG)
try:
    import cli
except Exception as e:
    logger.warning("failed to import cli module")

def configure_smart_licensing(email, idtoken, throughput):
    license_status = False
    throughput_status = False
    if idtoken is None:
        logger.warning("idtoken value is None. Please provide valid idtoken")
        return False

    smart_licensing_configuration = '''
    service call-home
    call-home
    contact-email-addr {}
    profile "CiscoTAC-1"
    active
    destination transport-method http
    no destination transport-method email
    destination address http https://tools.cisco.com/its/service/oddce/services/DDCEService
    '''.format(email)
    logger.info("Trying to configure smart licensing. Configs: {}".format(smart_licensing_configuration))
    for i in range(5):
        cli.configurep(smart_licensing_configuration)
        cli.executep('license smart register idtoken {}'.format(idtoken))
        cli.configurep('platform hardware throughput level MB {}'.format(throughput))
        time.sleep(30)
        output = cli.cli('show license summary')
        logger.info("Output of show license summary: {}".format(output))
        if "Status: REGISTERED" in output:
            logger.info("Smart licensing successful")
            license_status = True
        output = cli.cli('sh platform hardware throughput level')
        logger.info("Throughput level set to: {}".format(output))
        if str(throughput) in output:
            logger.info("Throughput level set successfully")
            throughput_status = True
        if license_status and throughput_status:
            logger.info("Successfully configured Smart Licensing and Throughput level")
            return True
    
    logger.info("There were some issues with configuring Smart Licensing or Throughput level which did not succeed after 5 attempts. Please review configuration")
    return False
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to Configure Smart licensing on CSR")
    parser.add_argument('--email',
                        help='provide email address for smart licensing. default is sch-smart-licensing@cisco.com',
                        action='store',
                        dest='email', default='sch-smart-licensing@cisco.com')
    parser.add_argument('--idtoken', action='store', dest='idtoken', 
                        help='provide account idtoken string')
    parser.add_argument('--throughput', help='provide desired throughtput level in MB. default is 2500',
                        action='store',
                        dest='throughput', default='2500')
    args = parser.parse_args()
    logger.info("idtoken: {}".format(args.idtoken))
    logger.info("throughput: {}".format(args.throughput))
    logger.info("email: {}".format(args.email))
    configure_smart_licensing(args.email, args.idtoken, args.throughput)
