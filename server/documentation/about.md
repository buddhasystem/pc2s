#### The Objective
The objective is to discover, locate and deliver
units of *conditions and calibrations data* of a particular
type as requested by the client, which are considered valid
at a particular point in time and relevant to a certiain type of
processing of the experiment's data.
Logically, the overall system is a tandem of a **metadata service**
and a **data delivery** system. The data delivery can be implemented
using a number of suitable technologies (Apache, nginx, CVMFS etc or
even a combination of these platforms).

These two components are weakly coupled. The only connection between
them is the requiment that the metadata component needs to provide a
valid URL pointing to a data product to be shipped to the consumer by
the data delivery part. This provides considerable flexibility in implementation stage.

The PC2S project comprises the metadata service component. Web pages
on this site are a Web interface to that service, and are complemented by a suite
of command line clients.

#### Portable Conditions and Calibrations Service (PC2S)
PC2S stands for *"portable conditions and calibration service"*.
The "portable" aspect implies that

* the system is experiment-agnostic
* it can be installed trivially on most Linux platforms

Conditions and calibrations data are treated in the same manner
in PC2S since the semantics of their use is virtually identical
in most applications. Calibrations can be updated many times (as
opposed to the conditions data recorded once), however both form
input for processing jobs, discoverable through metadata.

#### Design principles

The PC2S design closely follows the philosopy and recommendations
developed in the HEP community for the conditions database systems.
General design principles for such systmes are
presented in a recent HSF paper: <https://arxiv.org/abs/1901.05429>

In many cases (such as in the Belle II Conditions database)
there is separation of the metadata and data delivery domains.
In practice, this means that the *data content* (i.e. the "payload")
is stored and delivered separately from the **database**
used to keep the *location* of these data - essentially a *metadata* system.
By quering the database the client (or the user) gets a URL pointing the
location of the data, from which it can be retrieved using the HTTP(S)
protocol or any other comparable means.

#### ERD
The ERD of the system is presented in the diagram below.
It is a simplified version of the design detailed in the
HSF paper cited above, and only contains a minimal set of
object attributes necessary to make its functionality possible.
Additional attributes can be added trivially as needed. One
non-trivial distinction between PC2S and the HSF model is
merging of the payload and IOV objects, done in order to
simplify the system.

![](/static/images/PC2S_ERD_v2.png"PC2S EDR")

#### Objects

* **Global Tag**
    * Serves as a handle for the entirety of the conditions and calibrations
    data created for a particular purpose, e.g. production for a particular time period or a
    specific Monte Carlo campaign.
* **Global Tag Map**
    * A simple object which helps manage which types of data (*"Tags"*, see below) are included
    in a particular Global Tag. The content of a *Global Tag* are managed by creation, deletion
    or modification of the relevant *Global Tag Map* objects.
* **Tag**
    * This object is used to denote a particular type of data (e.g. EMCal calibrations etc) and also specify
    the time limit of these data validity, i.e. the expiry of validity. The name of the corresponding
    attribute is "until".
* **Payload**
    * Direct reference to actual data (calibrations or conditions) via URL. In practice this
    often means a URL pointing to a NGINX server (optionally with a HA proxy) which is set
    up to efficiently deliver the data to the client. The payload object contains
    the timestamp of the *start* of its *Interval of Validity*. The name of the corresponding
    attribute is "since". By convention, there is no expiry timestamp in the payload object.
    It is expired automatically by the next payload in the time series, according to its "since"
    values. The *Payload* object also contains a sha256 value for the actual payload file, helping
    in debugging and content validation. This object is always tied to a specific *Tag* by design,
    so it can't exist meaningfully as a standalone entity. When a *Tag* is deleted from the database,
    all *Payload* records are deleted as well. Keep in mind that this only applies to the database
    records, while the payload data on disk is managed separately.

#### Example

Let's assume that a user wishes to record and later use dead channel maps
for the Electromagnetic Calorimeter (EMCal). The [PC2S CLI clients](/clients)
will be used for that purpose (please see the link for details of the API).
All clients are equipped with the "-h" options which produces a help screen.

**Create a tag**

The name is immaterial, but it may be useful to make it
recognizable e.g. *EMCalDeadMap* or similar. The **tag.py" client
will be used for this purpose, with two arguments - the desired name
of the tag and the time of its expiry (i.e. the time after which the tag
is considered definitely invalid).
```bash
./tag.py -c -n EMCalDeadMap -u '2024-12-25 22:50:50+00:00'
```
Here "-c" stands for "create", "-n" for "name" and "-u" for "until".
Note the correct format of the timestamp, which is timezone-aware.

**Register payloads**

Let's assume that the dead channel maps were produced by the appropriate
software and exist as four separate files, named deadmap[1-4].root.
The files are then placed on the data delivery system (not in the scope
of this discussion) and at this point are assigned valid URLs. For demonstration
purposes, let's assume the URLs follow the pattern:
*https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root* etc.

We will use the "payload.py" client to assign these payloads to the tag:
```bash
./payload.py -c -t EMCalDeadMap -i '2024-01-01 00:00:00+00:00' \
-u https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root \
-s 0309d592920880cce3a86d6b70d0fb87668de893f2b7792970853c26d6ede95c
```
Here "-c" stands for "create", "-t" for "tag" (which we defined as the one
we just created), the "-i" is is the start of the interval of validity, and
"-s" is the sha256 hash of the payload, i.e. the file deadmap1.root. It is
used to (a) provide a unique key to the payload (b) resolve situations where
same file name was used more than once by mistake.

The command above will be repeated four times, each time with an appropriate
file name and the checksum, and of course timestamp for each file, corresponding
the start of its vailidity. There is no expiry date for the payloads, as by
design the next one will automatically expire the previous.

The tag *EMCalDeadMap* and its associated payloads will be then visible in the
monitor screen (see the "Tags") entry in the left had side navigation bar.

**Create a Global Tag**

Let's now create a Global Tag wiith a descriptive name, e.g. "sPHENIX2024":
```bash
./gt.py -c -n sPHENIX2024
```
This global tag can contain any number of different types of data relevant
for the EMCal, e.g. channel gains, pedestals etc. We'll limit our example
to just one tag which is the dead channel map.

**Assign the Tag to the Global Tag**

We will use the "global tag map" client to associate this particular tag
- EMCalDeadMap - with the Global Tag "EMCal".
```bash
./gtm.py -c -n emcaldead -g sPHENIX2024 -t EMCalDeadMap -v 1
```
Additional tags can be assigned as necessary to the Global Tag in
a similar manner. The tags can also be detached from a Global Tag by
removing the corresponding Global Tag Map objects.


#### Implementation

PC2S is a Web application based on the Django framework and written
in Python (verison 3.9 was originally used). Included are both
the Web client for monitoring and exploring the database contents, and the
CLI client suite used to manipulate the database content. At the time of writing,
the data delivery portion (e.g. an instance of a *nginx* service) has not yet
been established and will be finalized later.

Sample requirements (as they are set in the virtual environment):
```bash
asgiref==3.3.1
Django==3.1.5
django-tables2==2.4.0
Markdown==3.3.4
pytz==2020.5
PyYAML==5.4.1
sqlparse==0.4.1
```
