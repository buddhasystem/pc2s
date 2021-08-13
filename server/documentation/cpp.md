# C++ Interface to PC2S

The C++ interface to PC2S uses the popular *curl* library to
interact with the service, using the same set of URLs and conventions
as the Python interface. 
Currently it exists as a C++ aplication prototype
which can be refactored into a library if needed. It retrieves conditions
data from a remote server, based on the *Metadata* that includes:

* The name of the *Global Tag*
* The type of the payload data to be retrieved i.e. a *Tag*
* A timestamp of the point in time when this data is expected
to be valid

It makes two HTTP connections in the process:

1. To the PC2S Metadata server, retrieving the URL of the payload
based on the parameters listed above
2. To the data delivery service with the URL thus obtained, and
retrieves the payload by downloading it to a local file.

The core of the C++ code interfacing the Metadata service
is outlined (roughly) as follows:

```c++
        // This line gets the reponse from the server:
        curl_easy_setopt(curl, CURLOPT_URL, c_url_pc2s);
        //---
        // snip
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write2string);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string)
```

The server response *response_string* is then parsed uding the *yaml-cpp* package.
