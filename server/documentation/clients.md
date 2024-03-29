# Python Interface

PC2S is a Web service. Accordigly, all interaction between the software clients
and the service is through HTTP. For interaction with PC2S a simple Python module
called **serverAPI**  has been created, with the following features:

* It is based on the popular *urllib* package.
* It contains a number of helper functions facilitating interaction with the service,
which can be as simple is a one-line function call.
* There is a map of internal client method calls to the Web service URLs,
which makes it easier to evolve the system without breaking the interface. For example,
the client itself never has to generate URLs or use hardcoded strings for that purpose.

For example, getting a list of Global Tags in a Python client looks something like that:
```python
API  = serverAPI(server='http://pc2s.sphenix.bnl.gov:80/', 0)
resp = API.simple_get('cdb', 'gtlist')
```
The module can be incorporated into any Python application as needed.

## CLI client utilities

PC2S comes with a suite of CLI utilities (clients) written in Python and
based on the **serverAPI** module. They support the entirety of its
functionality, i.e. it's possible to create and/or delete any object in
the system's data model. In addition, it is possible to make modifications
to certain objects after they are created, for example:

* Global Tags can be renamed.
* Tags can be renamed, while preserving references to other objects e.g. payloads and Global Tags.
* The *until* timestamp of the Tag obejct can be modified if needed.
---

### The "-h" option
The CLI utilities are self-documented - they are equipped with the "-h" option producing a help
screen. The output is presented below. For examples of the CLI usage please see the [corresponding page](/examples).

### Global Tag

```bash
usage: gt.py [-h] [-S SERVER] [-c] [-d] [-r] [-l] [-t] [-n NAME] [-N NEWNAME] [-q QUERY] [-s STATUS] [-y [YAML_FILE]] [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Global Tag
  -d, --delete          Delete a Global Tag
  -r, --rename          Rename a Global Tag
  -l, --list_gt         List names of all Global Tags
  -t, --tag_list        List names of tags in a Global Tag
  -n NAME, --name NAME  Global Tag Name
  -N NEWNAME, --newname NEWNAME
                        New Global Tag Name (for renaming)
  -q QUERY, --query QUERY
                        Partial Name to narrow down the list of Global Tags
  -s STATUS, --status STATUS
                        Set status: NEW, INV, PUB
  -y [YAML_FILE], --yaml_file [YAML_FILE]
                        YAML definition
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level

```

---

### Global Tag Map

```bash
usage: gtm.py [-h] [-S SERVER] [-c] [-d] [-n NAME] [-g GLOBAL_TAG] [-t TAG]
              [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Global Tag Map
  -d, --delete          Delete a Global Tag Map
  -n NAME, --name NAME  Global Tag Map Name
  -g GLOBAL_TAG, --global_tag GLOBAL_TAG
                        Global Tag Name
  -t TAG, --tag TAG     Tag Name
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
```

---

### Tag

```bash
usage: tag.py [-h] [-S SERVER] [-c] [-d] [-r] [-U] [-m] [-n NAME] [-N NEWNAME]
              [-u UNTIL] [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Tag
  -d, --delete          Delete a Tag
  -r, --rename          Rename a Tag
  -U, --usage           Useful tips
  -m, --modify          Modify the timestamp
  -n NAME, --name NAME  Tag Name
  -N NEWNAME, --newname NEWNAME
                        New Tag Name (for renaming)
  -u UNTIL, --until UNTIL
                        Valid until
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
```

---

### Payload

```bash
usage: payload.py [-h] [-S SERVER] [-c] [-d] [-f] [-U] [-n [NAME]] [-t TAG] [-i IOV] [-u URL] [-T TIME] [-g GLOBAL_TAG]
                  [-v VERBOSITY] [-p [POPULATE]]

optional arguments:
  -h, --help            show this help message and exit
  -S SERVER, --server SERVER
                        server URL: defaults to http://localhost:8000/
  -c, --create          Create a Payload
  -d, --delete          Delete a Payload
  -f, --fetch           Fetch a payload, by hash or (Global Tag, Tag, time)
  -U, --usage           Useful tips
  -n [NAME], --name [NAME]
                        name
  -t TAG, --tag TAG     tag
  -i IOV, --iov IOV     start of IOV ('since')
  -u URL, --url URL     url
  -T TIME, --time TIME  time
  -g GLOBAL_TAG, --global_tag GLOBAL_TAG
                        Global Tag name
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level
  -p [POPULATE], --populate [POPULATE]
                        For testing only: number of simulated records to create, with random IOVs. Requires a tag name.
```

