# Tan F. Wong 12/19/2023

import vitis
import os

# Create a client object
client = vitis.create_client()

# Set workspace 
workspace = os.path.expanduser('~')+'/workspace'
os.chdir(workspace)
client.set_workspace(workspace)

# Create platform
platform_name = 'rfsoc_adc_vitis_platform'
platform_description = 'A Vitis extensible platform with 1 ADC for the RFSoC4x2 board'
platform_hw = 'rfsoc_adc_hardware/rfsoc_adc_hardware.xsa'
xrt_domain_name = 'linux_xrt'

platform = client.create_platform_component(name=platform_name, desc=platform_description, \
                                            hw=platform_hw, emulation_xsa_path=platform_hw, \
                                            cpu="psu_cortexa53", no_boot_bsp=True, \
                                            os="linux", domain_name=xrt_domain_nam)
