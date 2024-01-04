# Tan F. Wong 12/19/2023

import vitis
import os
import shutil

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
platform_hw_emu = 'rfsoc_adc_hardware/rfsoc_adc_hardware_emu.xsa'
platform_domain = 'xrt'
linux_image_dir = workspace+'/rfsoc-linux/images/linux/'
platform_fsbl = 'zynqmp_fsbl.elf'
platform_pmu = 'pmufw.elf'

platform = client.create_platform_component(name=platform_name, desc=platform_description, \
                                            hw=platform_hw, emulation_xsa_path=platform_hw_emu, \
                                            cpu='psu_cortexa53', no_boot_bsp=True, \
                                            fsbl_path=platform_fsbl, pmufw_Elf=platform_pmu,\
                                            os='linux', domain_name=platform_domain)


# Copy boot files to boot_dir
boot_dir = workspace+'/'+platform_name+'/resources/xrt/boot/'
os.mkdir(boot_dir)
qemu_dir = workspace+'/'+platform_name+'/resources/xrt/qemu/'
shutil.copy(linux_image_dir+'bl31.elf', boot_dir+'bl31.elf')
shutil.copy(linux_image_dir+'bl31.elf', qemu_dir+'bl31.elf')
shutil.copy(linux_image_dir+'pmufw.elf', boot_dir+'pmufw.elf')
shutil.copy(linux_image_dir+'pmufw.elf', qemu_dir+'pmufw.elf')
shutil.copy(linux_image_dir+'u-boot.elf', boot_dir+'u-boot.elf')
shutil.copy(linux_image_dir+'u-boot.elf', qemu_dir+'u-boot.elf')
shutil.copy(linux_image_dir+'system.dtb', boot_dir+'system.dtb')
shutil.copy(linux_image_dir+'system.dtb', qemu_dir+'system.dtb')
shutil.copy(linux_image_dir+'zynqmp_fsbl.elf', boot_dir+'zynqmp_fsbl.elf')
shutil.copy(linux_image_dir+'boot.scr', boot_dir+'boot.scr')

# Add info to domain
domain = platform.get_domain(platform_domain)
domain.add_boot_dir(boot_dir)
#:domain.set_sd_dir(boot_dir)
domain.add_qemu_data(qemu_dir)

# Generate BIF 
# For some unknown reason
# domain.generate_bif()
# doesn't seem to work. So generate the BIF ourselves
lines = [\
  '/* linux */',\
  'the_ROM_image:',\
  '{',\
  '  [fsbl_config] a53_x64',\
  '  [bootloader] <'+boot_dir+platform_fsbl+'>',\
  '  [pmufw_image] <'+boot_dir+platform_pmu+'>',\
  '  [destination_device=pl] <bitstream>',\
  '  [destination_cpu=a53-0, exception_level=el-3, trustzone] <atf,'+boot_dir+'bl31.elf>',\
  '  [load=0x00100000] <dtb,'+boot_dir+'system.dtb>',\
  '  [destination_cpu=a53-0, exception_level=el-2] <uboot,'+boot_dir+'u-boot.elf>',\
  '}'
]
bif = boot_dir+'linux.bif'
with open(bif, 'w') as f:
    for line in lines:
        f.write(f"{line}\n")
f.close()
domain.add_bif(bif)

# Generate emulation argument files
# All these may not serve any propose as Vitis 2023.2.1 doesn't seem to support
# hardware emulation for 
lines = ['-M', 'arm-generic-fdt', '-serial', 'mon:stdio',\
         '-global', 'xlnx,zynqmp-boot.cpu-num=0',\
         '-global', 'xlnx,zynqmp-boot.use-pmufw=true',\
         '-net', 'nic','-net', 'user',\
         '-device',\
         'loader,addr=0xfffc0000,data=0x584c4e5801000000,data-be=true,data-len=8',\
         '-device',\
         'loader,addr=0xfffc0008,data=0x0000081000000000,data-be=true,data-len=8',\
         '-device',\
         'loader,addr=0xfffc0010,data=0x1000000000000000,data-be=true,data-len=8',\
         '-device',\
         'loader,addr=0xffd80048,data=0xfffc0000,data-len=4,attrs-secure=on',\
         '-device', 'loader,addr=0x100000,file=<system.dtb>',\
         '-device', 'loader,file=<bl31.elf>,cpu-num=0',\
         '-device', 'loader,file=<u-boot.elf>',\
         '-boot', 'mode=5']
qemu = qemu_dir+'qemu_args.txt'
with open(qemu, 'w') as f:
    for line in lines:
        f.write(f"{line}\n")
f.close()
domain.add_qemu_args(qemu_option = "PS", path=qemu)

lines = ['-M', 'microblaze-fdt',\
         '-device', 'loader,file=<pmufw.elf>',\
         '-machine-path', '.',
         '-display', 'none']
pmu = qemu_dir+'pmu_args.txt'
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





