# Port <em>Vitis Platform Creation Tutorial for ZCU104</em> to RFSoC4x2
My first experiment is to port the [Vitis Platform Creation Tutorial
for
ZCU104](https://github.com/Xilinx/Vitis-Tutorials/tree/2023.1/Vitis_Platform_Creation/Design_Tutorials/02-Edge-AI-ZCU104)
to the RFSoC4x2 board. 

## Step 1: Install the board files for RFSoC4x2
1. Get the board files from the [RealDigital repo](https://github.com/RealDigitalOrg/RFSoC4x2-BSP)
    ```shell
    git clone https://github.com/RealDigitalOrg/RFSoC4x2-BSP.git ~/workspace/RFSoC4x2-BSP
    ```
    The board files are in  `~/workspace/RFSoC4x2-BSP/board_files/rfsoc4x2`.
  
2. Add the board files to Vivado:
    Add the following line to Vivado startup script `~/.Xilinx/Vivado/Vivado_int.tcl` (if the file doesn't exist, add it):
    ```tcl
    set_param board.repoPaths [list "~/workspace/RFSoC4x2-BSSP"]
    ```


