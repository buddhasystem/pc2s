#### The Objective
The objective is to discover, locate and deliver
units of *conditions and calibrations data* of a particular
type as requested by the client, which are considered valid
at a particular point in time and relevant to a certiain type of
processing of the experiment's data.
Logically, the overall system is a tandem of a **metadata service**
and a **data delivery** system. Data delivery can be implemented
using a number of suitable technologies: HTTP (Apache, nginx etc),
CVMFS, XRootD or even a combination of these platforms, as needed.

These two components are weakly coupled. The only connection between
them is the requiment that the metadata component needs to provide a
valid URL pointing to a data product to be shipped to the consumer by
the data delivery part. This provides considerable flexibility in implementation stage.

The PC2S project comprises the metadata service component. Web pages
on this site are a Web interface to that service, and are complemented by a suite
of [command line clients](/clients). Examples of the PC2S use can be
found on the [corresponding page](/examples).

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

![](/static/images/PC2S_ERD_v3.png"PC2S EDR")

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
    values.

#### Time reference
PC2S is using timezone-aware DateTime objects. In the current version the UTC
timezone is utilized to reduce ambiguity. A valid string representation of
time (as required in certain client commands) follows the pattern illustrated
by this string:
```
2026-07-21 22:50:50+00:00
```
The section of the string following the "+" sign represents the offset due
to the time zone. In case of UTC as illustrated here it is simply 00:00.

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
