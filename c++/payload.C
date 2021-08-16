//-------------------------------------------------
//
// A simple demo of a C++ client interacting
// with a Web server and parsing the YAML response,
// getting the URL of a conditions data payload,
// then downloading the corresponding file.
//
//-------------------------------------------------

#include <iostream>
#include <yaml.h>

#include <curl/curl.h>
#include <string>

#include "lyra.hpp"

using namespace std;

size_t write2string(void* ptr, size_t size, size_t nmemb, std::string* data) {
    data->append((char*)ptr, size * nmemb);
    return size * nmemb;
}

size_t write2file(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    size_t written = fwrite(ptr, size, nmemb, stream);
    return written;
}
// #####################
int main(int argc, char* argv[])
{
    bool verbose            =   false;

    std::string server      =   "localhost:8000";
    std::string globaltag   =   "";
    std::string tag         =   "";
    std::string time        =   "";
    std::string output      =   "testfile.dat";


    auto cli = lyra::cli()
        | lyra::opt(verbose)
            ["-v"]["--verbose"]
            ("verbose" )
        | lyra::opt(server, "server" )
            ["-S"]["--server"]
            ("server")
        | lyra::opt(globaltag, "globaltag" )
            ["-g"]["--globaltag"]
            ("globaltag")
        | lyra::opt(tag, "tag" )
            ["-t"]["--tag"]
            ("tag")
        | lyra::opt(time, "time" )
            ["-T"]["--time"]
            ("time")
        | lyra::opt(output, "output" )
            ["-o"]["--output"]
            ("output");

    auto result = cli.parse( { argc, argv } );
    if ( !result ) {
	    std::cerr << "Error in command line: " << result.errorMessage() << std::endl;
	    exit(1);
    }

    if(verbose) {
        cout << "**** Verbose mode activated ****"  << endl;
        cout << "****      CLI parameters    ****"  << endl;
        cout << "server: "      << server           << endl;
        cout << "globaltag: "   << globaltag        << endl;
        cout << "tag: "         << tag              << endl;
        cout << "time:  "       << time             << endl;
        cout << "output:  "     << output           << endl;
        cout << "********************************"  << endl;
    }


    curl_global_init(CURL_GLOBAL_DEFAULT);
    auto curl = curl_easy_init();

    if (curl) {

        // Got the parameters, proceed to form query:
        const char* c_time = time.c_str();
        std::string encoded_time = curl_easy_escape(curl, c_time , 0);

        std::string url = "http://"+server+"/cdb/payload?globaltag="+globaltag+"&tag="+tag+"&time="+encoded_time;

        if(verbose) {
            cout << "Metadata Server query URL: " << url << endl;
        }

        const char* c_url = url.c_str();

        // This line gets the reponse from the server:
        curl_easy_setopt(curl, CURLOPT_URL, c_url);
        //---

        curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
        curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 50L);
        curl_easy_setopt(curl, CURLOPT_TCP_KEEPALIVE, 1L);

        std::string response_string;
        std::string header_string;

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write2string);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &header_string);

        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
        curl_global_cleanup();

        curl = NULL;

        if(verbose) {
            cout << "Response from the server:\n"
            << response_string << "----------------"
            << endl;
        }

    YAML::Node node = YAML::Load(response_string);

    std::string payload_url = node["url"].as<std::string>();
    if(verbose) {
        std::cout << "Payload URL: " << payload_url << "\n";
    }

    const char* c_url_payload = payload_url.c_str();
    // Example:
    // const char* c_url_payload = "https://opendata.cern.ch/record/15011/files/ERTntup_ggntuple.root";

    std::cout<< c_url_payload <<endl;

    auto curl = curl_easy_init();
    FILE *fp;
    CURLcode res;

    if (curl) {
        fp = fopen(output.c_str(),"wb");
        curl_easy_setopt(curl, CURLOPT_URL, c_url_payload);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write2file);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
        res = curl_easy_perform(curl);
        /* always cleanup */
        curl_easy_cleanup(curl);
        curl_global_cleanup();
        fclose(fp);
       }
    }

}

// -----------------------------------------------------------------------------
// --- ATTIC ---
//    std::cout << "Hello World!" << "\n";
//    YAML::Node node = YAML::Load("[1, 2, 3]");
//    std::cout << node[0] << node[1];
//    "http://localhost:8000/cdb/globaltag/list"

//        for (std::size_t i=0; i<node.size(); i++) {
//            std::cout << "!" << node[i]["name"] << "\n";
//        }
// cout << curl_easy_escape(curl, "2024-05-01 02:01:14+00:00" , 0) << endl;;