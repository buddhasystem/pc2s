<hr>

#### Introductory Note
Please note that all examples presented here are for demonstration
purposes, all object names and attributes shown here are arbitrary
and only for illustration.

#### Example 1: Look up and Explore a Global Tag
Obtain a listing of all Global Tags in the systems, in YAML format:
```bash
$ ./gt.py -l
- name: gt_test
- name: sPHENIX2024
- name: ECCE_MC_2023
```
Look at the list of tags included in a particular Global Tag:
```bash
$ ./gt.py -n sPHENIX2024 -t
name: sPHENIX2024
tags:
- EMCalDeadMap
- IHCalDeadMap
```
Look at the contents of a particular tag:
```bash
name: EMCalDeadMap
until: 2024-12-24 22:50:50+00:00
globaltags:
- sPHENIX2024
payloads:
- sha26: 0309d592920880cce3a86d6b70d0fb87668de893f2b7792970853c26d6ede95c
  since: 2024-01-01 00:01:59+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root
- sha26: 21eb8c9fd4d3b795c39f08d565ff5d3d019455e7a16001a1e81c08d94a602e8b
  since: 2024-03-01 00:01:01+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap2.root
- sha26: 0fc352fd32dd7a616082974a067702d4faed3770ad8624f94ffbfb89653539d2
  since: 2024-06-01 00:05:01+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap3.root
- sha26: e3afbd1c1557c3fa3b14fc6d7a3fdd24a1c53e3abd91205f9b8c198ff5bb9f5d
  since: 2024-09-01 01:01:15+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap4.root
```
Things to note:

* There is a list of all Global Tags referencing this particular tag. In this case,
there is only one Global Tag, "sPHENIX2024".
* There is a list of payloads included in this YAML output, with complete information
about each payload.


<hr>

#### Example 2: Create and Populate a Global Tag

Let's assume that a user wishes to record and later use dead channel maps
for the Electromagnetic Calorimeter (EMCal). The [PC2S CLI clients](/clients)
will be used for that purpose (please see the link for details of the API).
All clients are equipped with the "-h" options which produces a help screen.

**Create a tag**

The name of the tag we are about to create is immaterial, but it may be useful
to make it recognizable e.g. *EMCalDeadMap* or similar. The *tag.py* client
will be used for this purpose, with two arguments - the desired name
of the tag and the time of its expiry (i.e. the time after which the tag
is considered definitely invalid).
```bash
$ ./tag.py -c -n EMCalDeadMap -u '2024-12-25 22:50:50+00:00'
```
Here "-c" stands for "create", "-n" for "name" and "-u" for "until".
Note the correct format of the timestamp, which is timezone-aware.

**Register payloads**

Let's assume that the dead channel maps were produced by the appropriate
EMCal software and exist as four separate files, named deadmap[1-4].root.
The files are then placed on the data delivery system (not in the scope
of this discussion) and at this point are assigned valid URLs. For demonstration
purposes, let's assume the URLs follow the pattern:
*https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root* etc.
PC2S does not have any requirements as to the specific pattern of URLs.

We will use the "payload.py" client to assign these payloads to the tag:
```bash
$ ./payload.py -c -t EMCalDeadMap -i '2024-01-01 00:00:00+00:00' \
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
$ ./gt.py -c -n sPHENIX2024
```
This global tag can contain any number of different types of data relevant
for the EMCal, e.g. channel gains, pedestals etc. We'll limit our example
to just one tag which is the dead channel map.

**Assign the Tag to the Global Tag**

We will use the "global tag map" client to associate this particular tag
- EMCalDeadMap - with the Global Tag "EMCal".
```bash
$ ./gtm.py -c -n emcaldead -g sPHENIX2024 -t EMCalDeadMap -v 1
```
Additional tags can be assigned as necessary to the Global Tag in
a similar manner. The tags can also be detached from a Global Tag by
removing the corresponding Global Tag Map objects.

Global tags can be created at any point in time, even before
their content (i.e. tags) are decided upon.

