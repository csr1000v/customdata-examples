#!/usr/bin/env python

"""
This module/script can be used to set the smart license on C8000V device in cloud.

Please note this script reboots after setting the license to set the boot level.
After bootlevel is set, user can configure the throughput using "platform hardware throughput level MB <value>"

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

def configure_smart_licensing(idtoken, bootlevel):
    license_status = False
    throughput_status = False
    if idtoken is None:
        logger.warning("idtoken value is None. Please provide valid idtoken")
        return False

    smart_licensing_configuration = '''
    license smart transport smart
    license smart url smart  https://smartreceiver.cisco.com/licservice/license
    '''
    boot_level_config = '''
    license boot level {} addon dna-premier
    '''.format(bootlevel)
    logger.info("Trying to configure smart licensing. Configs: {}".format(smart_licensing_configuration))
    for i in range(5):
        logger.info("In FOR loop: i is {}".format(i))
        logger.info("executing smart_licensing_configuration")
        cli.configurep(smart_licensing_configuration)
        logger.info("executing license smart trust idtoken command..")
        cli.executep('license smart trust idtoken {} local'.format(idtoken))
        #logger.info("executing boot_level_config")
        #cli.configurep(boot_level_config)
        #time.sleep(30)
        logger.info("executing show license tech support | inc ENABLED")
        output = cli.cli('show license tech support | inc ENABLED')
        logger.info("Output of show license summary: {}".format(output))
        if "Smart Licensing is ENABLED" in output:
            logger.info("Enabling Smart licensing is successful. ")
            logger.info('Please reboot using reload command to set the boot level. When CSR comes up, configure the Throughput using "platform hardware throughput level MB <value>" command')
            license_status = True
            cli.configurep('platform hardware throughput level MB 250')
            #cli.executep('reload')
            return True
    
    logger.warning("There were some issues with configuring Smart Licensing which did not succeed after 5 attempts. Please review configuration")
    return False
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to Configure Smart licensing on CSR")
    parser.add_argument('--idtoken', action='store', dest='idtoken', 
                        help='provide account idtoken string')
    parser.add_argument('--bootlevel', choices=['Network-Advantage', 'Network-Essentials', 'Network-Premier'], 
                        help='provide desired boot level',
                        action='store',
                        dest='bootlevel', default='Network-Premier')
    args = parser.parse_args()
    logger.info("idtoken: {}".format(args.idtoken))
    logger.info("bootlevel: {}".format(args.bootlevel))
    configure_smart_licensing(args.idtoken, args.bootlevel)
