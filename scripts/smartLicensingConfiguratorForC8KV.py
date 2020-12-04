#!/usr/bin/env python

"""
This module/script can be used to set the smart license on C8000V device in cloud.

Please note it is REQUIRED to configure "license boot level <value>" on the device for this script to work.

If you are passing this script in customdata/userdata, below is the example on how to pass via userdata section. 
Note that along with "Section: scripts" "Section: license" is REQUIRED

Section: license
techpackage:<value>

Section: scripts
https://raw.githubusercontent.com/csr1000v/customdata-examples/master/scripts/smartLicensingConfiguratorForC8KV.py --idtoken <value> --throughput <value>

"""
import argparse
import logging
import time
FORMAT = '%(asctime)20s:%(module)15s:%(funcName)20s:%(lineno)4s - %(levelname)7s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('smartLicensingConfiguratorForC8KV')
logger.setLevel(logging.DEBUG)
try:
    import cli
except Exception as e:
    logger.warning("failed to import cli module")

def configure_smart_licensing(idtoken, throughput):
    license_status = False
    throughput_status = False
    if idtoken is None:
        logger.warning("idtoken value is None. Please provide valid idtoken")
        return False

    smart_licensing_configuration = '''
    license smart transport smart
    license smart url smart  https://smartreceiver.cisco.com/licservice/license
    '''
    logger.info("Trying to configure smart licensing. Configs: {}".format(smart_licensing_configuration))
    for i in range(5):
        cli.configurep(smart_licensing_configuration)
        cli.executep('license smart trust idtoken {} local'.format(idtoken))
        cli.configurep('platform hardware throughput level MB {}'.format(throughput))
        output = cli.cli('show license tech support | inc ENABLED')
        if "Smart Licensing is ENABLED" in output:
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
    
    logger.warning("There were some issues with configuring Smart Licensing which did not succeed after 5 attempts. Please review configuration")
    return False
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to Configure Smart licensing on CSR")
    parser.add_argument('--idtoken', action='store', dest='idtoken', 
                        help='provide account idtoken string')
    parser.add_argument('--throughput', help='provide desired throughtput level in MB. default is 2500',
                        action='store',
                        dest='throughput', default='2500')
    args = parser.parse_args()
    logger.info("idtoken: {}".format(args.idtoken))
    logger.info("throughput: {}".format(args.throughput))
    configure_smart_licensing(args.idtoken, args.throughput)
