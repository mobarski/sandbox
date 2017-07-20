# P7


### P7 overview

P7 is a parallelization microframework / set of utilities similar to Hadoop Streaming but limited to single machine only. 

The name (P7) is a numeronym (abbreviation) for the word **parallel**.


### P7 components

* **p7map** - mapper/combiner job executor
* **p7red** - reducer/combiner job executor
* **p7res** - resource manager
* **p7cat** - parallel concatenation of files


### p7map

```
usage: p7x4m5.py [-h] [-i I] [-b B] [-o O] [-e E] [-p P] [-n N] mapper

P7 streaming utility - run command in parallel

positional arguments:
  mapper      mapper command

optional arguments:
  -h, --help  show this help message and exit
  -i I        head buffer size for input data pump (1024)
  -b B        buffer size for subprocess (4096)
  -o O        path template for stdout, must contain {0} which will be
              replaced by partition id (mapper{0}.out)
  -e E        path template for stderr (logs), must contain {} which will be
              replaced by partition id (mapper{}.log)
  -p P        ouput pipe command (TODO)
  -n N        number of mapper jobs (4)
```

### p7red

```
usage: p7red.py [-h] [-i I] [-o O] [-e E] [-c C] reducer

p7red - P7 reducer job executor

positional arguments:
  reducer     reducer command

optional arguments:
  -h, --help  show this help message and exit
  -i I        paths for stdin
  -o O        path for stdout
  -e E        path for stderr (logs)
  -c C        combiner command
```

### p7cat

```
TODO
```

### p7res

```
TODO
```
