import sys
import os
import msvcrt



ofh = int(sys.argv[1])
ofd = msvcrt.open_osfhandle(ofh,0)
print('OFH',ofh)
print('OFD',ofd)
fo = os.fdopen(ofd,'wb')
fo.write(sys.stdin.read().upper())
fo.flush()
