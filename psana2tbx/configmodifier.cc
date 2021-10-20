/* 
READ THIS BEFORE USE!
 This won't work out of the box since it writes ShapesData.hh private
 variable. 
 1. You need to make NameInfo _NameInfo; public (comment out
 line 261).
 2. Add/change following to CMakeList

add_executable(configmodifier
    configmodifier.cc
)
target_link_libraries(configmodifier
    xtc
)

install(TARGETS xtcwriter smdwriter xtcreader amiwriter configmodifier
    EXPORT xtcdataTargets
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)
*/


#include <fcntl.h>
#include <map>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <unistd.h>
#include <iostream>
#include <sys/time.h>
#include <fstream>
#include <array>

// additions from xtc writer
#include <type_traits>
#include "xtcdata/xtc/XtcFileIterator.hh"
#include "xtcdata/xtc/VarDef.hh"
#include "xtcdata/xtc/DescData.hh"
#include "xtcdata/xtc/Dgram.hh"
#include "xtcdata/xtc/TypeId.hh"
#include "xtcdata/xtc/XtcIterator.hh"
#include "xtcdata/xtc/Smd.hh"

using namespace XtcData;
using std::string;
using namespace std;

#define BUFSIZE 0x4000000

class DebugIter : public XtcIterator
{
public:
    enum { Stop, Continue };
    int new_segment_id = 0;
    DebugIter() : XtcIterator()
    {
    }

    void set_new_segment_id(int segment_id){
        new_segment_id = segment_id;
    }

    void get_value(int i, Name& name, DescData& descdata){
        int data_rank = name.rank();
        int data_type = name.type();
        printf("%d: %s rank %d, type %d\n", i, name.name(), data_rank, data_type);

        switch(name.type()){
        case(Name::UINT8):{
            if(data_rank > 0){
                Array<uint8_t> arrT = descdata.get_array<uint8_t>(i);
                printf("%s: %d, %d, %d\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %d\n",name.name(),descdata.get_value<uint8_t>(i));
            }
            break;
        }

        case(Name::UINT16):{
            if(data_rank > 0){
                Array<uint16_t> arrT = descdata.get_array<uint16_t>(i);
                printf("%s: %d, %d, %d\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %d\n",name.name(),descdata.get_value<uint16_t>(i));
            }
            break;
        }

        case(Name::UINT32):{
            if(data_rank > 0){
                Array<uint32_t> arrT = descdata.get_array<uint32_t>(i);
                printf("%s: %d, %d, %d\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %d\n",name.name(),descdata.get_value<uint32_t>(i));
            }
            break;
        }

        case(Name::UINT64):{
            if(data_rank > 0){
                Array<uint64_t> arrT = descdata.get_array<uint64_t>(i);
                printf("%s: %llu, %llu, %llu\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %llu\n",name.name(),descdata.get_value<uint64_t>(i));
            }
            break;
        }

        case(Name::INT8):{
            if(data_rank > 0){
                Array<int8_t> arrT = descdata.get_array<int8_t>(i);
                printf("%s: %d, %d, %d\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %d\n",name.name(),descdata.get_value<int8_t>(i));
            }
            break;
        }

        case(Name::INT16):{
            if(data_rank > 0){
                Array<int16_t> arrT = descdata.get_array<int16_t>(i);
                printf("%s: %d, %d, %d\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %d\n",name.name(),descdata.get_value<int16_t>(i));
            }
            break;
        }

        case(Name::INT32):{
            if(data_rank > 0){
                Array<int32_t> arrT = descdata.get_array<int32_t>(i);
                printf("%s: %d, %d, %d\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %d\n",name.name(),descdata.get_value<int32_t>(i));
            }
            break;
        }

        case(Name::INT64):{
            if(data_rank > 0){
                Array<int64_t> arrT = descdata.get_array<int64_t>(i);
                printf("%s: %lld, %lld, %lld\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %lld\n",name.name(),descdata.get_value<int64_t>(i));
            }
            break;
        }

        case(Name::FLOAT):{
            if(data_rank > 0){
                Array<float> arrT = descdata.get_array<float>(i);
                printf("%s: %f, %f\n",name.name(),arrT.data()[0],arrT.data()[1]);
                    }
            else{
                printf("%s: %f\n",name.name(),descdata.get_value<float>(i));
            }
            break;
        }

        case(Name::DOUBLE):{
            if(data_rank > 0){
                Array<double> arrT = descdata.get_array<double>(i);
                printf("%s: %f, %f, %f\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %f\n",name.name(),descdata.get_value<double>(i));
            }
            break;
        }

        case(Name::CHARSTR):{
            if(data_rank > 0){
                Array<char> arrT = descdata.get_array<char>(i);
                printf("%s: \"%s\"\n",name.name(),arrT.data());
                    }
            else{
                printf("%s: string with no rank?!?\n",name.name());
            }
            break;
        }

        case(Name::ENUMVAL):{
            if(data_rank > 0){
                Array<int32_t> arrT = descdata.get_array<int32_t>(i);
                printf("%s: %d, %d, %d\n",name.name(),arrT.data()[0],arrT.data()[1], arrT.data()[2]);
                    }
            else{
                printf("%s: %d\n",name.name(),descdata.get_value<int32_t>(i));
            }
            break;
        }

        case(Name::ENUMDICT):{
            if(data_rank > 0){
                printf("%s: enumdict with rank?!?\n", name.name());
            } else{
                printf("%s: %d\n",name.name(),descdata.get_value<int32_t>(i));
            }
            break;
        }
        }
    }

    int process(Xtc* xtc)
    {
        switch (xtc->contains.id()) {
        case (TypeId::Parent): {
            iterate(xtc);
            break;
        }
        case (TypeId::Names): {
            Names& names = *(Names*)xtc;
            _namesLookup[names.namesId()] = NameIndex(names);
            Alg& alg = names.alg();


            // Modify segment id for hsd
            char* det_hsd = "hsd";
            int result;
            result = strcmp(names.detName(), det_hsd);
            if (result == 0){
                names._NameInfo.segment = new_segment_id;
                printf("*** DetName: %s, Segment %d, DetType: %s, Alg: %s, Version: 0x%6.6x, Names:\n",
                   names.detName(), names._NameInfo.segment, names.detType(),
                   alg.name(), alg.version());
            } else {
                printf("*** DetName: %s not modified\n", names.detName());
            }

            for (unsigned i = 0; i < names.num(); i++) {
                Name& name = names.get(i);
                printf("Name: %s Type: %d Rank: %d\n",name.name(),name.type(), name.rank());
            }

            break;
        }
        case (TypeId::ShapesData): {
            ShapesData& shapesdata = *(ShapesData*)xtc;
            // lookup the index of the names we are supposed to use
            NamesId namesId = shapesdata.namesId();
            // protect against the fact that this xtc
            // may not have a _namesLookup
            if (_namesLookup.count(namesId)<0) break;
            DescData descdata(shapesdata, _namesLookup[namesId]);
            Names& names = descdata.nameindex().names();
            Data& data = shapesdata.data();
        printf("Found %d names\n",names.num());
            for (unsigned i = 0; i < names.num(); i++) {
                Name& name = names.get(i);
                get_value(i, name, descdata);
            }
            break;
        }
        default:
            break;
        }
        return Continue;
    }

private:
    NamesLookup _namesLookup;
};

void show(Dgram& dg) {
    printf("%s transition: time %d.%09d, env 0x%u, "
           "payloadSize %d extent %d\n",
           TransitionId::name(dg.service()), dg.time.seconds(),
           dg.time.nanoseconds(),
           dg.env, dg.xtc.sizeofPayload(),dg.xtc.extent);
    DebugIter dbgiter;
    dbgiter.iterate(&(dg.xtc));
}

void usage(char* progname)
{
  fprintf(stderr, "Usage: %s -f <filename> [-h]\n", progname);
}

#define MAX_FNAME_LEN 256

int main(int argc, char* argv[])
{
    /*
    * The smdwriter reads an xtc file, extracts
    * payload size for each event datagram,
    * then writes out (fseek) offset in smd.xtc2 file.
    */
    int c;
    int parseErr = 0;
    char* xtcname = 0;
    int new_segment_id =0;

    while ((c = getopt(argc, argv, "hf:s:")) != -1) {
    switch (c) {
      case 'h':
        usage(argv[0]);
        exit(0);
        break;
      case 'f':
        xtcname = optarg;
        break;
      case 's':
        new_segment_id = atoi(optarg);
        break;
      default:
        parseErr++;
    }
    }

    if (!xtcname) {
    usage(argv[0]);
    exit(2);
    }

    // Read input xtc file
    int fd = open(xtcname, O_RDONLY);
    if (fd < 0) {
    fprintf(stderr, "Unable to open file '%s'\n", xtcname);
    exit(2);
    }

    XtcFileIterator iter(fd, BUFSIZE);
    Dgram* dgIn;

    // Writing out data
    void* buf = malloc(BUFSIZE);
    unsigned nodeId=512; // choose a nodeId that the DAQ will not use.  this is checked in addNames()
    NamesLookup namesLookup;
    NamesId namesId(nodeId, 0);

    printf("\nModify config and write back.\n");

    Dgram* dgOut;
    dgIn = iter.next();
    dgOut = (Dgram*)buf;
    
    // Copy the header and payload
    memcpy(dgOut, dgIn, sizeof(*dgIn));
    memcpy(dgOut->xtc.payload(), dgIn->xtc.payload(), dgIn->xtc.sizeofPayload());
    

    // Iterate through xtc and update segment id for hsd
    DebugIter dbgiter;
    dbgiter.set_new_segment_id(new_segment_id);
    dbgiter.iterate(&(dgOut->xtc));
    
    ::close(fd);

    fstream s(xtcname); // use option std::ios_base::binary if necessary
    s.seekp(0, std::ios_base::beg);
    char* my_data = (char *)dgOut;
    s.write(my_data, sizeof(*dgOut) + dgOut->xtc.sizeofPayload());
    
    free(buf);

    return 0;

}
