#### Design principles

<!-- ![foo!](/static/images/sphenix-logo-black-bg.png "San Juan Mountains") -->

The system design closely follows the philosopy and recommendations
developed in the HEP community for the conditions database systems.

The overarching principle of these designs is separation of the
metadata and data delivery domains - 
for the most part the *data content* (i.e. the "payload")
is stored and delivered separately from the **database**
used to keep the *location* of these data. In a nutshell, this means that by
quering the database the client (or the user) gets a URL pointing
the location of the data, from which it can be retrieved using
the HTTP(S) protocol or any other comparable means.

#### The Data Model
##### Conditions vs Calibrations
In practice, most steps in a production process require
specific sets of conditions and/or calibrations data. Semantics
of the conditions vs calibrations are virtually identical in that
these are sets of parameters necessary to process a particular
body of data, thus forming the static part of a particular process
input. In the following there will be no distinction made between
the "conditions" and "calibarations" types of data.

##### Object Entities


#### CLI client utilities
PC2S comes with a complete suite of clients supporting the full
spectrim of its functionality

<hr/>

##### Global Tag
```bash
usage: gt.py [-h] [-S SERVER] [-c] [-d] [-l] [-t] [-n NAME] [-s STATUS]
             [-y [YAML_FILE]] [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Global Tag
  -d, --delete          Delete a Global Tag
  -l, --list_gt         List names of all Global Tags
  -t, --tag_list        List names of tags in a Global Tags
  -n NAME, --name NAME  Global Tag Name
  -s STATUS, --status STATUS
                        Status to be set
  -y [YAML_FILE], --yaml_file [YAML_FILE]
                        YAML definition
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
```
<hr/>

##### Global Tag Map
```bash
usage: gtm.py [-h] [-S SERVER] [-c] [-d] [-n NAME] [-g GLOBAL_TAG] [-t TAG]
              [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Global Tag
  -d, --delete          Delete a Global Tag
  -n NAME, --name NAME  Global Tag Map Name
  -g GLOBAL_TAG, --global_tag GLOBAL_TAG
                        Global Tag Name
  -t TAG, --tag TAG     Tag
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
```

<hr/>

##### Tag
```bash
usage: tag.py [-h] [-S SERVER] [-c] [-d] [-U] [-n NAME] [-u UNTIL]
              [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Tag
  -d, --delete          Delete a Tag
  -U, --usage           Useful tips
  -n NAME, --name NAME  Tag Name
  -u UNTIL, --until UNTIL
                        Valid until
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
```
<hr/>

##### Payload
```bash
usage: payload.py [-h] [-S SERVER] [-c] [-d] [-f] [-U] [-s [SHA256]] [-t TAG]
                  [-i IOV] [-u URL] [-T TIME] [-g GLOBAL_TAG] [-v VERBOSITY]
                  [-p [POPULATE]]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Payload
  -d, --delete          Delete a Payload
  -f, --fetch           Fetch a payload, by hash or Global Tag and time value
  -U, --usage           Useful tips
  -s [SHA256], --sha256 [SHA256]
                        sha256
  -t TAG, --tag TAG     tag
  -i IOV, --iov IOV     start of IOV ('since')
  -u URL, --url URL     url
  -T TIME, --time TIME  time
  -g GLOBAL_TAG, --global_tag GLOBAL_TAG
                        Global Tag name
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
  -p [POPULATE], --populate [POPULATE]
                        For testing only: number of simulated records to
                        create, with random IOVs. Requires a tag name.
```


