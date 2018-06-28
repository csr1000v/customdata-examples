#!/usr/bin/env python
import argparse
import logging
import os
import datetime
import time

FORMAT = '%(asctime)20s:%(module)15s:%(funcName)20s:%(lineno)4s - %(levelname)7s - %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('smartLicensingConfigurator')
logger.setLevel(logging.DEBUG)

try:
    import cli
except Exception as e:
    logger.warning("not able to import cli module")
    logger.exception(e)

def report_drops(entries):
    home = os.path.expanduser('~')
    output_dir = home + "dropsReporterOutput"
    try:
        os.makedirs(output_dir)
    except Exception as e:
        logger.exception(e)

    output_file = output_dir + "/drops_report.txt"
    curtime = datetime.datetime.now()

    with open(output_file, 'wa') as f:
        f.write( str(curtime) + " : " + entries )

def execute_command(command):
    cmd_output = cli.execute(command)
    while len(cmd_output) == 0:
        logger.warning("CMD FAILED, retrying")
        cmd_output = cli.execute(command)
    return cmd_output

def get_stat_drop():
    for i in range(2):
        try:
            cmd_output = execute_command(
                "show platform hardware qfp active statistics drop clear")

            for line in cmd_output.splitlines():
                if ("-" in line) or ("Global Drop Stats" in line):
                    continue

                entries = line.split()
                output_line = "%s --> %s/%s" % (entries[0], entries[1], entries[2])
                logger.info(output_line)
                report_drops(output_line)
                break
        except Exception as e:
            logger.exception(e)
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="packets drops reporter script that reports packets drops")

    parser.add_argument('--drops', action='store_true', default=True,
                        help='capture drops from show platform hardware qfp active statistics drop clear command')

    args = parser.parse_args()
    while args.drops:
        get_stat_drop()
        # sleep for 5 minutes
        time.sleep(300)
