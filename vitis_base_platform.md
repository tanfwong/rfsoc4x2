# Port <em>Vitis Platform Creation Tutorial for ZCU104</em> to RFSoC4x2
My first experiment is to port the [Vitis Platform Creation Tutorial
for
ZCU104](https://github.com/Xilinx/Vitis-Tutorials/tree/2023.1/Vitis_Platform_Creation/Design_Tutorials/02-Edge-AI-ZCU104)
to the RFSoC4x2 board. 

## Step 0: Install the board files for RFSoC4x2
1. Get the board files from the [RealDigital repo](https://github.com/RealDigitalOrg/RFSoC4x2-BSP)
    ```shell
    git clone https://github.com/RealDigitalOrg/RFSoC4x2-BSP.git ~/workspace/RFSoC4x2-BSP
    ```
    The board files are in  `~/workspace/RFSoC4x2-BSP/board_files/rfsoc4x2`.
  
2. Add the board files to Vivado:
    Add the following line to Vivado startup script `~/.Xilinx/Vivado/Vivado_int.tcl` (if the file doesn't exist, add it):
    ```tcl
    set_param board.repoPaths [list "<full path to home directory>/workspace/RFSoC4x2-BSP"]
    ```
## Step 1: Create a Vivado Hardware Design
Follow the steps in [Vitis Platform Creation Tutorial
for
ZCU104-Step 1](https://github.com/Xilinx/Vitis-Tutorials/blob/2023.1/Vitis_Platform_Creation/Design_Tutorials/02-Edge-AI-ZCU104/step1.md) to generate the hardware `.xsa` files by selecting the RFSoC4x2 board instead when creating the Vivado project. 

I named the Vivado project `rfsoc_base_hardware` in `~/workspace` and generated the files:
- `rfsoc_base_hardware.xsa` for hardware
- `rfsoc_base_hardware_emu.xsa` for hardware emulation

## Step 2: Create a Vitis Platform
1. Download and install the ZYNQMP common image from [Xilinx's download page](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-platforms.html). Untar it to a directory of choice:
    ```shell
    tar xzf xilinx-zynqmp-common-v2023.1.tar.gz -C ~/workspace
    ```
2. Install the `sysroot`:
    ```shell
    cd ~/workspace/xilinx-zynqmp-common-v2023.1
    ./sdk.sh -d ./sysroot
    ```

3. Create a Vitis Platform project:
