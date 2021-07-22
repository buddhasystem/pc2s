# pc2s client

This folder contains code, configuration and other materials
for the pc2s client.

# Testing the scripts
```python
./payload.py -s `sha256sum ../README.md | awk '{print $1}'`
./payload.py -c -s `date | sha256sum  | awk '{print $1}'` -u "file://`realpath README.md`" -t foo -i "2026-07-21 22:50:50+00:00"
```
