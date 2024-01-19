import xml.etree.ElementTree as ET
from B import *
import xml.etree.ElementTree as ET

import xml.etree.ElementTree as ET

def parse_can_frame_definition(can_frame):
    name = can_frame.get('Name')
    dlc = can_frame.get('Dlc')
    frame_id = can_frame.get('Id')

    print(f"Frame Name: {name}, DLC: {dlc}, ID: {frame_id}")

    pdus_node = can_frame.find('.//Pdus')
    if pdus_node is not None:
        # Check for DynamicContainerPduDefinition
        dynamic_container = pdus_node.find('.//DynamicContainerPduDefinition')
        if dynamic_container is not None:
            dlc_dynamic_container = dynamic_container.get('Dlc')
            header_dynamic_container = dynamic_container.find('Header').text
            print(f"  Dynamic Container - DLC: {dlc_dynamic_container}, Header: {header_dynamic_container}")

            # Iterate through SignalPduDefinition nodes within DynamicContainerPduDefinition
            for signal_pdu in dynamic_container.findall('.//SignalPduDefinition'):
                dlc_signal_pdu = signal_pdu.get('Dlc')
                dynamic_properties = signal_pdu.find('.//DynamicPduProperties')
                pdu_id = dynamic_properties.find('PduId').text
                time_period = dynamic_properties.find('TimePeriod').text
                time_offset = dynamic_properties.find('TimeOffset').text

                print(f"    Signal PDU - DLC: {dlc_signal_pdu}, PDU ID: {pdu_id}, Time Period: {time_period}, Time Offset: {time_offset}")

                # Iterate through Signals nodes within SignalPduDefinition
                signals_node = signal_pdu.find('.//Signals')
                if signals_node is not None:
                    for signal in signals_node.findall('.//SignalDefinition'):
                        signal_name = signal.get('Name')
                        start_bit = signal.find('StartBit').text
                        bit_length = signal.find('BitLength').text

                        print(f"      Signal Name: {signal_name}, Start Bit: {start_bit}, Bit Length: {bit_length}")

                        table_values_node = signal.find('.//TableValues')
                        if table_values_node is not None:
                            # Extract Key and Value from TableValues node
                            table_values = [(item.get('Key'), item.get('Value')) for item in table_values_node.findall('.//Item')]
                            # signal_info['TableValues'] = table_values
                            print(table_values)

                        # Check if LinearComputationMethod node exists
                        linear_computation_method_node = signal.find('.//LinearComputationMethod')
                        if linear_computation_method_node is not None:
                            factor = linear_computation_method_node.find('.//Factor/DynamicValue').text
                            offset = linear_computation_method_node.find('.//Offset/DynamicValue').text
                            print( {'Factor': factor, 'Offset': offset})
                            # signal_info['LinearComputationMethod'] = {'Factor': factor, 'Offset': offset}

def parse_xml(xml_data):
    root = ET.fromstring(xml_data)

    # Iterate through CanFrameDefinition elements
    for can_frame in root.findall('.//CanFrameDefinition'):
        parse_can_frame_definition(can_frame)
        print("\n")

# Your XML data
# xml_data = """
# <Frames>
#     <!-- ... (your XML data) ... -->
# </Frames>
# """

# Call the function to parse XML
parse_xml(xml_data)

