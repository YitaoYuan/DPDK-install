# Introdution

This is an automatic installation script for DPDK.

It installs DPDK locally and relies on environment-modules to manage the multi-version environment.

It support DPDK with version >= 20. 

# Usage

1. Put `setup.py` under a folder like this.

```
.
├── pkg
│   ├── dpdk-20.11.10.tar.xz
│   ├── dpdk-21.11.7.tar.xz
│   ├── dpdk-22.11.5.tar.xz
│   └── dpdk-23.11.tar.xz
└── setup.py
```

2. Edit `setup.py`, change variable `root`.  This changes the place for both building and installation.

3. Run the script (with no arguments).

# Load DPDK

use `module load dpdk/<version>`

## Note 

Since environment-modules relies on environment variables to choose paths. 
Using it with `sudo` may cause troubles because `sudo` will change the user and corresponding environment variables.
One can use `sudo -E` to preserve environment variables but this does not preserve `LD_LIBRARY_PATH` and `PATH`.
As a patch, one can use commands like `sudo LD_LIBRARY_PATH=$LD_LIBRARY_PATH` in such occassion.
