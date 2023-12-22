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
platform_domain = 'xrt'
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
# doesn't seem to work. So generate the BIF ourselves
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
resources_path = workspace+'/'+platform_name+'/resources/'
bif = resources_path+'linux.bif'
with open(bif, 'w') as f:
    for line in lines:
        f.write(f"{line}\n")
f.close()
domain.add_bif(bif)

# Generate emulation argument files
lines = ['-M', 'arm-generic-fdt', '-serial', 'mon:stdio',\
         '-global', 'xlnx,zynqmp-boot.cpu-num=0',\
         '-global', 'xlnx,zynqmp-boot.use-pmufw=true', '-net', 'nic',\
         '-device', 'loader,file=<bl31.elf>,cpu-num=0',\
         '-device', 'loader,file=<u-boot.elf>',\
         '-boot', 'mode=5']
qemu = resources_path+'qemu_args.txt'
with open(qemu, 'w') as f:
    for line in lines:
        f.write(f"{line}\n")
f.close()
domain.add_qemu_args(qemu_option = "PS", path=qemu)
domain.add_qemu_data(linux_image_dir)

lines = ['-M', 'microblaze-fdt',\
         '-device', 'loader,file=<pmufw.elf>',\
         '-machine-path', '.',
         '-display', 'none']
pmu = resources_path+'pmu_args.txt'
with open(pmu, 'w') as f:
    for line in lines:
        f.write(f"{line}\n")
f.close()
domain.add_qemu_args(qemu_option = "PMU", path=pmu)


# Build platform
platform.build()

# Report info
platform.report()
domain.report()

# Close the client connection and terminate the vitis server
vitis.dispose()





