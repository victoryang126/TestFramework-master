import xml.etree.ElementTree as ET
from B import *
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET

def parse_signal_definition(signal):
    signal_name = signal.get('Name')
    start_bit = signal.find('StartBit').text
    bit_length = signal.find('BitLength').text

    # Initialize a dictionary to store signal information
    signal_info = {
        'Name': signal_name,
        'StartBit': start_bit,
        'BitLength': bit_length,
    }

    # Check if TableValues node exists
    table_values_node = signal.find('.//TableValues')
    if table_values_node is not None:
        # Extract Key and Value from TableValues node
        table_values = [(item.get('Key'), item.get('Value')) for item in table_values_node.findall('.//Item')]
        signal_info['TableValues'] = table_values

    # Check if LinearComputationMethod node exists
    linear_computation_method_node = signal.find('.//LinearComputationMethod')
    if linear_computation_method_node is not None:
        factor = linear_computation_method_node.find('.//Factor/DynamicValue').text
        offset = linear_computation_method_node.find('.//Offset/DynamicValue').text
        signal_info['LinearComputationMethod'] = {'Factor': factor, 'Offset': offset}

    return signal_info

def parse_signal_pdu_definition(signal_pdu):
    signal_pdu_name = signal_pdu.get('Name')
    dlc_signal_pdu = signal_pdu.get('Dlc')

    # Initialize a dictionary to store Signal PDU information
    signal_pdu_info = {
        'Name': signal_pdu_name,
        'Dlc': dlc_signal_pdu,
    }

    # Check if DynamicContainerPduDefinition node exists
    dynamic_container_pdu_node = signal_pdu.find('.//DynamicContainerPduDefinition')
    if dynamic_container_pdu_node is not None:
        dlc_dynamic_container_pdu = dynamic_container_pdu_node.get('Dlc')
        header_dynamic_container_pdu = dynamic_container_pdu_node.get('Header')
        signal_pdu_info['DynamicContainerPdu'] = {
            'Dlc': dlc_dynamic_container_pdu,
            'Header': header_dynamic_container_pdu,
        }

    # Check if Signals node exists
    signals_node = signal_pdu.find('.//Signals')
    if signals_node is not None:
        # Initialize a list to store Signal definitions
        signals_info = []
        # Iterate through SignalDefinition nodes within Signals node
        for signal in signals_node.findall('.//SignalDefinition'):
            signal_info = parse_signal_definition(signal)
            signals_info.append(signal_info)

        signal_pdu_info['Signals'] = signals_info

    return signal_pdu_info

def parse_can_frame_definition(can_frame):
    can_frame_name = can_frame.get('Name')
    dlc_can_frame = can_frame.get('Dlc')

    # Check if Id element exists
    id_can_frame = can_frame.get('Dlc')
    # id_can_frame = id_element.text if id_element is not None else None

    can_frame_info = {
        'Name': can_frame_name,
        'Dlc': dlc_can_frame,
        'Id': id_can_frame,
    }

    pdus_node = can_frame.find('.//Pdus')
    if pdus_node is not None:
        pdus_info = []
        for signal_pdu in pdus_node.findall('.//SignalPduDefinition'):
            pdu_info = parse_signal_pdu_definition(signal_pdu)
            pdus_info.append(pdu_info)

        can_frame_info['Pdus'] = pdus_info

    return can_frame_info

tree = ET.parse('test.xml')
root = tree.getroot()

can_frames = root.findall('.//CanFrameDefinition')

parsed_can_frames = []

for can_frame in can_frames:
    parsed_can_frame = parse_can_frame_definition(can_frame)
    parsed_can_frames.append(parsed_can_frame)

for can_frame_info in parsed_can_frames:
    print(can_frame_info)
