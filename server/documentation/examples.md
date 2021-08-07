<hr>
#### Example 1: Look up and Explore a Global Tag
Obtain a listing of all Global Tags in the systems, in YAML format - names shown here
are arbitrary and only serve illustration purposes:
```bash
./gt.py -l
- name: gt_test
- name: sPHENIX2024
- name: ECCE_MC_2023
```
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
./tag.py -c -n EMCalDeadMap -u '2024-12-25 22:50:50+00:00'
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

Global tags can be created at any point in time, even before
their content (i.e. tags) are decided upon.

