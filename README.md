# PC2S: Portable Conditions and Calibrations Service

## The objective
The aim of the project is to realize a lightweight, fully portable, configurable,
experiment-agnostic service for the Conditons and Calibrations data.
It was inspired in part by the Belle II CDB and is based on recommendations
of the HEP Software Foundation, closely following the suggested data model.

## Components

PC2S consists of two web services working in tandem, and
client software. The two web services are

* The PC2S Metadata server
* The Data Delivery service included as a simple nginx-based test server in this repository.
The nginx server can be easily configured for the needs of the target experiment.

The role of the Metadata server is to locate the URLs of data payloads to
be delivered by the latter, based on queries from a client. Queries include:

* The name of the specific data aggregation to be queried i.e. the *"Global Tag"*.
Examples of such aggregation would be a Global Tag used in production for a certain
run-year, or a set of parameters for some Monte Carlo campaign
* The name of the Tag, identifying the *type* of data to be retrieved. For example,
this could be data describing pedestals in a calorimeter, or a corresponding
dead channel map
* A timestamp - the time at which the data is considered valid

If there is a data product satisfying the query the service returns
a response in YAML format, containing the **URL of the payload**. The client
then uses this URL to access to the payload, to be retrieved from the data
delivery service.

At the moment the clients interfacing the two services described above are
implemented in two languages:

* Python: includes a reusable interface package and a few CLI utilities based on it.
* C++: a simple prototype application demonstrating access to the service using that platform.

Both are based on the *urllib* library and using the same identical interface
of the the PC2S Metadata server.

## Evaluation of the System using Docker

### Outline of the setup

For a basic test of the funcionality of the system, the user needs to use
two Docker images, one for the PC2S Metadata service and its clients, and
another for the NGINX-based test instance of the data delivery service.

```bash
docker pull buddhasystem/pc2s-metadata:latest
docker pull buddhasystem/pc2s-nginx:latest
```

The *pc2s-metadata* image contains some mock metadata which will work
in conjunction with the content of the *pc2s-nginx* image. That is to
say that contents of a specific tag recorded in *pc2s-metadata* point
to valid files hosted on pc2s-nginx.

The NGINX image contains some test data in ROOT format that's useful
for basic testing. The content of these files is not relevant for this test.
The scope of the test is to run a PC2S client to get a proper URL and
then to download the correct file from the delivery service (NGINX).

### Start containers

Start a PC2S Metadata container exposing port 8000 to the host.
In this case 8000 to 8000 will do, provided it's not used by some
other service on your system. Other port numbers can be used, too.

```bash
# Start a PC2S Metadata (Django) container, exposing port 8000 as 8080 on the host machine:
docker run -p 8000:8000 pc2s-metadata

# Start a PC2S Data Delivery (NGINX) container, exposing port 80 as 8080 on the host machine:
docker run -it --rm -d -p 8080:80 pc2s-nginx
```

In this case, the container-internal port 80 is mapped to the host port 8080.
You can check that the ngnix service is live by pointing your browser to ```localhost:8080```
which should result in a basic landing page.

### Use CLI clients to interact with the Metadata Service

To start accessing the metadata service:

* Point your browser to *localhost:8000*.
* Connect to the running PC2S Metadata container by running interactive shell (bash), e.g. by using ```docker exec -it XXX bash``` where "XXX" is the hash of the running container. At the
prompt, the user will be in the "clients" directory, ready to use the Python client software
for testing.

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
