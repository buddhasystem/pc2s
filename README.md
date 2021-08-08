# pc2s: Portable Conditions and Calibrations Service

## The objective
The aim of the project is to realize a fully portable, configurable,
experiment-agnostic service for the Conditons and Calibrations data.
Part of it was inspired by the Belle II CDB, however there are significant
differences.

## Test-Driving the System using Docker
### Get the Image from Docker Hub
```bash
docker pull buddhasystem/pc2s:latest
```
### Create a Container
Start a pc2s container with port mapping, in this case 8000 to 8000 will do,
provided it's not used by some other service on your system. Other port
numbers can be used, too.
```bash
docker run -p 8000:8000 pc2s:latest
```


* Point your browser to "localhost:8000
* Connect to the running container by running interactive shell (bash)
* "cd clients"

## Misc
### TZ-aware parsing of time in Django
Example:
```python
temp_date=parse_datetime("2026-07-21 22:50:50+00:00")
```
...which results in
```python
datetime.datetime(2026, 7, 21, 22, 50, 50, tzinfo=datetime.timezone(datetime.timedelta(0), '+0000'))
```

