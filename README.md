# customdata-examples

This repository attempts to provide examples and scripts to help users easily write Customdata bootstrap Day0 Configuration for CSR1000v in Azure.

The official documentation of Customdata feature resides at:
https://www.cisco.com/c/en/us/td/docs/routers/csr1000/software/azu/b_csr1000config-azure.html

Scripts dir in this repository contains various scripts that can be provided in "Scripts" section of Customdata to achieve its purpose. List of Scripts and its purpose: 

packetsDropsReporter.py - Periodically (every 5 mins) checks the output of "show platform hardware qfp active statistics drop clear" and if finds any packet drops in cli output, writes the drop counts in ~/dropsReporterOutput/drops_report.txt.

smartLicensingConfigurator.py - It takes idtoken of your Cisco Smart Licensing account and Throughput level as Input. Configures Smart licensing on CSR with provided Throughput level.

Examples dir in this repository contains examples of Customdata bootstrap config files. 

