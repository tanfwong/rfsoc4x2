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
platform_domain = 'linux_xrt'
platform_fsbl = workspace+'/rfsoc-linux/images/linux/zynqmp_fsbl.elf'
platform_pmu = workspace+'/rfsoc-linux/images/linux/pmufw.elf'

platform = client.create_platform_component(name=platform_name, desc=platform_description, \
                                            hw=platform_hw, emulation_xsa_path=platform_hw, \
                                            cpu='psu_cortexa53', no_boot_bsp=True, \
                                            fsbl_path=platform_fsbl, pmufw_Elf=platform_pmu,\
                                            os='linux', domain_name=platform_domain)

# Add info to domain
boot_dir = workspace+'/'+platform_name+'/boot'
os.mkdir(boot_dir)
sd_dir = workspacce+'/rfsoc-linux/images/linux/'

domain = platform.get_domain(platform_domain)
domain.add_boot_dir(boot_dir)
domain.set_sd_dir(sd_dir)
domain.generate_bif()


