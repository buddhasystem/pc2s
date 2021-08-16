# PC2S C++ client demo

## About

A simple demo of a C++ client interacting with the PC2S system
to locate and download files, according to defined Intervals of Validity,
from an external source.

## Dependencies

* *Lyra* command-line argument parser, provided here as a self-contained header file with no other dependencies
* *yaml-cpp*, can be installed from GitHub (requires simple build)
* *liburl*, installed as sudo apt-get or a comparable method on Ubuntu, this may be **sudo apt-get install -y libcurl4-gnutls-dev**

## Build

```bash
g++ -o payload.exe -L /usr/local/lib -I /usr/local/include/yaml-cpp/ -I /usr/local/include/yaml-cpp/node --std=c++0x payload.C /usr/local/lib/libyaml-cpp.a  -lcurl
```

Environment variables can be set for convenience:

```bash
export CPATH=.:/usr/local/include/yaml-cpp/:/usr/local/include/yaml-cpp/node
export LD_LIBRARY_PATH=/usr/local/lib
g++ -o payload.exe --std=c++0x payload.C /usr/local/lib/libyaml-cpp.a  -lcurl
```

## Run

```bash
$ ./payload.exe -T '2024-06-07 02:01:14+00:00' -g sPHENIX2024 -t EMCalDeadMap  -o new.root
```

