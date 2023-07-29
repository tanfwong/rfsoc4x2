/**
* Copyright (C) 2019-2021 Xilinx, Inc
*
* Licensed under the Apache License, Version 2.0 (the "License"). You may
* not use this file except in compliance with the License. A copy of the
* License is located at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations
* under the License.
*/

/* Slightly modified by Tan F. Wong to serve as a simple example kernel to
* load streamed samples from the ADCC0 on ZU48DR to global memory.
* 7/20/2023
*/

#include "ap_int.h"
#include "ap_axi_sdata.h"

#define DATA_WIDTH 128

typedef ap_axis<DATA_WIDTH, 0, 0, 0> pkt;

extern "C" {
void dummy_kernel(ap_uint<DATA_WIDTH>* buffer0, hls::stream<pkt> &s_in, unsigned int size) {
#pragma HLS INTERFACE m_axi port = buffer0 bundle = gmem0
#pragma HLS INTERFACE axis port = s_in

// Auto-pipeline is going to apply pipeline to this loop
dummy:
    for (unsigned int i = 0; i < size; i++) {
#pragma HLS PIPELINE II = 1
        pkt value = s_in.read();
        buffer0[i] = value.data;
    }
}
}
