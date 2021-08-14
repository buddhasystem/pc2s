# PC2S: Portable Conditions and Calibrations Service

## The objective
The aim of the project is to realize a lightweight, fully portable, configurable,
experiment-agnostic service for the Conditons and Calibrations data.
It was inspired in part by the Belle II CDB and is based on recommendations
of the HEP Software Foundation, slosely following the suggested data model.

## Components

PC2S consists of two web services working in tandem, and
client software. The web services are

* the PC2S Metadata server
* the data delivery service (included as a simple test server in this repository)

The role of the former is to locate the URLs of data payloads to be delivered
by the latter, based on queries from a client. Queries include:

* The name of the aggregation to be queried i.e. the "Global Tag"
* The name of the Tag, identifying the type of data to be retrieved
* A timestamp - the time at which the data is considered valid

If there is a data product satisfying the query the service returns
a response in YAML format, containing the URL of the payload. The client
then has access to the payload, to be retrieved from the data delivery service
using the URL previouly obtained.

The clients are

* Python
* C++

Both are based on the *urllib* library and using the same identical interface
of the the PC2S Metadata server.

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
