import sys, os
# Append parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import proto.py.robot_state_pb2 as robot_state
import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher, ProtoPublisher

class BasicScript():
    """
        Send a protobuf on the given topic when calling execute(), it doesn't support multiple pb msg or with delay between them
        Must override execute() function with what it do
    """
    def __init__(self, script_name, topic_name, pb_msg) -> None:
        self.script_name = script_name
        ecal_core.initialize(sys.argv, script_name)
        self.pub = ProtoPublisher(topic_name, pb_msg)
        self.pb_msg = pb_msg
        pass
    def execute(self):
        self.pub.send(self.pb_msg)

def get_msg_types(pb_module):
    """_summary_

    Args:
        pb_module (_type_): Takes the python protobuf module object
    """
    return [x for x in pb_module.DESCRIPTOR.message_types_by_name.keys()]

def get_fields_from_msgtype(pb_module, msg_type: str):
    msg_type = getattr(pb_module, msg_type)
    msg_type.DESCRIPTOR.fields[0].full_name
    return [{'name':x.name, 'type':x.type} for x in msg_type.DESCRIPTOR.fields]
    #TODO : return type

    #conversion of type : 
    #SOURCE : https://github.com/protocolbuffers/protobuf/blob/main/python/google/protobuf/descriptor.py
    """
        TYPE_DOUBLE         = 1
        TYPE_FLOAT          = 2
        TYPE_INT64          = 3
        TYPE_UINT64         = 4
        TYPE_INT32          = 5
        TYPE_FIXED64        = 6
        TYPE_FIXED32        = 7
        TYPE_BOOL           = 8
        TYPE_STRING         = 9
        TYPE_GROUP          = 10
        TYPE_MESSAGE        = 11
        TYPE_BYTES          = 12
        TYPE_UINT32         = 13
        TYPE_ENUM           = 14
        TYPE_SFIXED32       = 15
        TYPE_SFIXED64       = 16
        TYPE_SINT32         = 17
        TYPE_SINT64         = 18
        MAX_TYPE            = 18
    """

#def get_all_msgs(pb_module):
    #fetch all messages with the fields available to make a GUI

if __name__ == "__main__":
    for msg_type in get_msg_types(robot_state):
        msg = get_fields_from_msgtype(robot_state, msg_type)
        print(msg_type)
        for field in msg:
            print(f"field named {field['name']} of type {field['type']}")