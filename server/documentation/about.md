#### Portable Conditions and Calobrations System (PC2S)
PC2S stands for *"portable conditions and calibration system"*.
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
    specific Monte Carlo campaign
* **Global Tag Map**
    * A simple object which helps manage which types of data ("tags", see below) are included
    in a particular Global Tag.
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
    It is expired automatically by the next payload in the time series, according to the "since"
    values.


