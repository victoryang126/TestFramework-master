import can
import cantools
import canmatrix

from can.io.blf import BLFReader

logs = BLFReader(r"AA_BenchNormal_EP.blf")

for  msg in logs:
    print(msg)