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
linux_image_dir = workspace+'/rfsoc-linux/images/linux/'
platform_fsbl = linux_image_dir+'zynqmp_fsbl.elf'
platform_pmu = linux_image_dir+'pmufw.elf'

platform = client.create_platform_component(name=platform_name, desc=platform_description, \
                                            hw=platform_hw, emulation_xsa_path=platform_hw, \
                                            cpu='psu_cortexa53', no_boot_bsp=True, \
                                            fsbl_path=platform_fsbl, pmufw_Elf=platform_pmu,\
                                            os='linux', domain_name=platform_domain)

# Add info to domain
sd_dir = workspace+'/'+platform_name+'/fat32'
os.mkdir(sd_dir)

domain = platform.get_domain(platform_domain)
domain.add_boot_dir(linux_image_dir)
domain.set_sd_dir(sd_dir)

# Generate BIF 
# For some unknown reason
# domain.generate_bif()
# doesn't seem to work. So the generate the BIF ourselves
lines = [\
  '/* linux */',\
  'the_ROM_image:',\
  '{',\
  '  [fsbl_config] a53_x64',\
  '  [bootloader] <'+platform_fsbl+'>',\
  '  [pmufw_image] <'+platform_pmu+'>',\
  '  [destination_device=pl] <bitstream>',\
  '  [destination_cpu=a53-0, exception_level=el-3, trustzone] <atf,'+linux_image_dir+'bl31.elf>',\
  '  [load=0x00100000] <dtb,'+linux_image_dir+'system.dtb>',\
  '  [destination_cpu=a53-0, exception_level=el-2] <uboot,'+linux_image_dir+'u-boot.elf>',\
  '}'
]
bif = workspace+'/'+platform_name+'/resources/linux.bif'
with open(bif, 'w') as f:
    for line in lines:
        f.write(f"{line}\n")

domain.add_bif(bif)

# Build platform
platform.build()





