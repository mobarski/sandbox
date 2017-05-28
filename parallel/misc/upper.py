import sys
import os

ofd = int(sys.argv[1])
print('OFD',ofd)
fo = os.fdopen(ofd,'wb')
fo.write(sys.stdin.read().upper())
fo.flush()
