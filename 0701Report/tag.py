import tarfile
files_to_pack = [r"C:\PyCharmProject\aria_py\Util"]
import PyQt5
output_targz = "C:\PyCharmProject\ApymUtil.tar.gz"

with tarfile.open(output_targz,'w:gz') as tar:
    for file in files_to_pack:
        tar.add(file)

import ApymUtil
