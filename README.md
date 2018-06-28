# customdata-examples

This repository provides examples and scripts to help users easily write Custom Data bootstrap Day0 Configuration for CSR1000v in Azure.

The official documentation of Custom Data feature resides at:
https://www.cisco.com/c/en/us/td/docs/routers/csr1000/software/azu/b_csr1000config-azure.html

## Scripts 
Scripts dir in this repository contains various scripts that can be provided in "Scripts" section of Customdata to achieve its purpose. List of Scripts and its purpose: 

* [```packetDropsReporter.py```](scripts/packetDropsReporter.py) - Periodically (every 5 mins) checks the output of "show platform hardware qfp active statistics drop clear" and if finds any packet drops in cli output, writes the drop counts in ~/dropsReporterOutput/drops_report.txt.

* [```smartLicensingConfigurator.py```](scripts/smartLicensingConfigurator.py)- It takes idtoken of your Cisco Smart Licensing account and Throughput level as Input. Configures Smart licensing on CSR with provided Throughput level.

## Examples
Examples dir in this repository contains examples of Custom Data bootstrap config files. Any of the examples in Examples dir can be used as a input to Custom Data for CSR in Azure. 

E.g., To launch a CSR with [```customdata1.txt```](examples/customdata1.txt) as a input to Custom data for CSR in Azure use --custom-data argument.
      az vm create -n <vm_name> -g <rg_name> --image cisco:cisco-csr-1000v:16_7:16.7.120171201 --custom-data customdata1.txt

* [```customdata1.txt```](examples/customdata1.txt) - This sample Custom Data bootstrap files provides an example of how to use following Sections - "IOS configuration", "Python package" and "Scripts". If this example bootstrap file provided as a input to Custom data for CSR in Azure, It will achieve the following on first boot up - Day 0:
1. Configure the CSR with Configuration commands provided in section - 'IOS configuration'
2. Run the [```packetDropsReporter.py```](scripts/packetDropsReporter.py) script in Guestshell.
3. Install python package csr_azure_guestshell with --user argument.
