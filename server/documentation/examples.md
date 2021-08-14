# CLI Examples

Please note that all examples presented here are for demonstration
purposes, all object names and attributes shown here are arbitrary
and only for illustration. In the examples below it is assumed
that the clients interact with the service using the default server
URL i.e. *localhost:8000". If another service address is needed (which
is certainly the case in realistic scenarios) one needs to add the "-S"
option to set the correct server location, for example:

```bash 
$ ./gt.py -l -S 'http://pc2s.sphenix.bnl.gov:80/'
```

## Example 1: Look up and Explore a Global Tag
Obtain a listing of all Global Tags in the systems, in YAML format:

```bash
$ ./gt.py -l
- name: gt_test
- name: sPHENIX2024
- name: ECCE_MC_2023
```

Look at the list of tags included in a particular Global Tag, "sPHENIX2024":

```bash
$ ./gt.py -n sPHENIX2024 -t
name: sPHENIX2024
tags:
- EMCalDeadMap
- IHCalDeadMap
```

Look at the contents of a particular tag:

```bash
$ ./tag.py -n EMCalDeadMap
name: EMCalDeadMap
until: 2024-12-24 22:50:50+00:00
globaltags:
- sPHENIX2024
payloads:
- name: deadmap1
  since: 2024-01-01 00:01:59+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root
- name: deadmap2
  since: 2024-03-01 00:01:01+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap2.root
- name: deadmap3
  since: 2024-06-01 00:05:01+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap3.root
- name: deadmap4
  since: 2024-09-01 01:01:15+00:00
  url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap4.root


```

Things to note:

* There is a list of all Global Tags referencing this particular tag. It is contained
in the attribute "globaltags". In this particular case, there is only one Global Tag "sPHENIX2024" which is referencing this Tag. It is entirely possible that there are more, in which case this secton of YAML will contain the respective names.
* There is a list of payloads included in this YAML output, with complete information
about each payload.

Now, let's get complete contents of a Global Tag, down to all payloads (which can be
a rather long list in a realistic scenario):

```bash
$ ./gt.py -n sPHENIX2024
name: sPHENIX2024
status: PUB
tags:
- name: EMCalDeadMap
  until: 2024-12-24 22:50:50+00:00
  globaltags:
  - sPHENIX2024
  payloads:
  - name: deadmap1
    since: 2024-01-01 00:01:59+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root
  - name: deadmap2
    since: 2024-03-01 00:01:01+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap2.root
  - name: deadmap3
    since: 2024-06-01 00:05:01+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap3.root
  - name: deadmap4
    since: 2024-09-01 01:01:15+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap4.root
- name: IHCalDeadMap
  until: 2024-12-24 22:50:50+00:00
  globaltags:
  - sPHENIX2024
  payloads:
  - name: ihcalmap1
    since: 2024-01-01 00:59:00+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/ihcal/deadmap1.root
  - name: ihcalmap2
    since: 2024-02-01 02:59:00+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/ihcal/deadmap2.root
  - name: ihcalmap3
    since: 2024-02-22 02:59:00+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/ihcal/deadmap3.root
  - name: ihcalmap4
    since: 2024-03-01 01:01:00+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/ihcal/deadmap4.root
  - name: ihcalmap5
    since: 2024-04-11 04:01:10+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/ihcal/deadmap5.root
  - name: ihcalmap6
    since: 2024-06-03 01:01:15+00:00
    url: https://nginx.sphenix.bnl.gov/cdb/ihcal/deadmap6.root
```

Now let's take a look at how a client obtains the location (URL)
of a particular type of the conditions/calibrations data, based on the Global Tag name
or a Global Tag name, and the timestamp relevant to the processing being done. Using the URL,
actual data can be reqiested from a Data Delivery service (separate from the PC2S proper).

```bash
$ ./payload.py -f -g sPHENIX2024 -t EMCalDeadMap -T '2024-05-01 02:01:14+00:00'
name: deadmap2
tag: EMCalDeadMap
since: 2024-03-01 00:01:01+00:00
url: https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap2.root
```

---

## Example 2: Create and Populate a Global Tag

Let's assume that a user wishes to record and later use dead channel maps
for the Electromagnetic Calorimeter (EMCal). The [PC2S CLI clients](/clients)
will be used for that purpose (please see the link for details of the API).
All clients are equipped with the "-h" options which produces a help screen.

### Create a tag

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

### Register payloads

Let's assume that the dead channel maps were produced by the appropriate
EMCal software and exist as four separate files, named deadmap[1-4].root.
Each file is valid during a certain time period, and is associated
with a timestamp corresponding to the start of its validity.
The files are then placed on the data delivery system (not in the scope
of this discussion) and at this point are assigned valid URLs. For demonstration
purposes, let's assume the URLs follow the pattern:
*https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root* etc.
PC2S does not have any requirements as to the specific pattern of URLs.

We will use the "payload.py" client to assign these payloads to the tag,
while recording the "since" timestamp i.e. the start of the file's contents
validity:

```bash
$ ./payload.py -c -t EMCalDeadMap -i '2024-01-01 00:00:00+00:00' \
-u https://nginx.sphenix.bnl.gov/cdb/emcal/deadmap1.root \
-n deadmap1
```

Here "-c" stands for "create", "-t" for "tag" (which we defined as the one
we just created), the "-i" is is the start of the interval of validity, and
"-n" is the name of the payload, i.e. the file deadmap1.root. This is a mneumonic
name that can be anything.

The command above can be repeated multiple times, each time with an appropriate
file name and of the timestamp for each file, corresponding
the start of its vailidity. There is no expiry date for the payloads, as by
design the next one will automatically expire the previous.

The tag *EMCalDeadMap* and its associated payloads will be then visible in the
monitor screen (see the "Tags") entry in the left had side navigation bar.

### Create a Global Tag

Let's now create a Global Tag wiith a descriptive name, e.g. "sPHENIX2024":

```bash
$ ./gt.py -c -n sPHENIX2024
```

At this point the Global Tag only acquired a name but no actual content/references.

Global Tags can contain any number of different types of data relevant
to any detector subsystem. In case of EMCal, these could be channel gain
values, pedestals etc. We'll limit our example to just one tag which
is the so-called *dead channel map*.

### Assign the Tag to the Global Tag

We will use the "global tag map" client to associate this particular tag
*EMCalDeadMap* with the Global Tag "EMCal".

```bash
$ ./gtm.py -c -n emcaldead -g sPHENIX2024 -t EMCalDeadMap

```

Additional tags can be assigned as necessary to any Global Tag in
a similar manner. *The tags can also be detached from a Global Tag by removing corresponding Global Tag Map objects*.

Global tags can be created at any point in time, even before
their content (i.e. tags they refer to) are decided upon.
