# GSRC Benchmark in Python

Very quick and even dirtier Reader for the
[GSRC](http://vlsicad.eecs.umich.edu/BK/GSRCbench/) Benchmark Dataset.

## Get the Dataset

Run the `resources/download.sh` script.

```
% pushd resources && ./download.sh && popd
```

This will generate a `./resources/gsrc/HARD` and `./resources/gsrc/SOFT`,
containing the respective datasets.

## Read the Data

See `example/example.py`:

```python
from gsrc import read_gsrc

base = './resources/gsrc'
mode = 'HARD'
name = 'n100'

data = read_gsrc(base,name,mode)
```

## Installation

From git:

```
% pip install git+https://github.com/augustunderground/pygsrc.git
```

From source:

```
% git clone https://github.com/augustunderground/pygsrc.git
% cd pygsrc
% pip install . --use-feature=in-tree-build
```
