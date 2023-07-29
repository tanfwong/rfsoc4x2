# Hacked out from the RFSoC-PYNQ distribution
# Tan F. Wong 7/20/2023

from xrfclk import set_ref_clks
from xrfclk.gpio import GPIO

# Seems to need these to turn on the LMK chip
lmk_reset = GPIO(341, 'out')
lmk_clk_sel0 = GPIO(342, 'out')
lmk_clk_sel1 = GPIO(346, 'out')

lmk_reset.write(1)
lmk_reset.write(0)
lmk_clk_sel0.write(0)
lmk_clk_sel1.write(0)

# Set LMK and LMX freq
set_ref_clks(lmk_freq=245.76, lmx_freq=491.52)
