import xml.etree.ElementTree as ET
import pandas as pd




class AcpdfUtil:

    @classmethod
    def parse_signal_table_values(cls, signal):
        """
        a function used to get the tables values for the signal node
        :param signal:
        :return:
        """
        table_values_node = signal.find('.//TableValues')
        if table_values_node is not None:
            # Extract Key and Value from TableValues node
            table_values = [f"{item.get('Key')}:{item.get('Value')}" for item in table_values_node.findall('.//Item')]
            return table_values
        return None



    @classmethod
    def parse_signal_linear_computation(cls, signal):
        """
        function used to get linear computation method for signal node
        :param signal:
        :return:
        """
        linear_computation_method_node = signal.find('.//LinearComputationMethod')
        if linear_computation_method_node is not None:
            factor = float(linear_computation_method_node.find('.//Factor/DynamicValue').text)
            offset = float(linear_computation_method_node.find('.//Offset/DynamicValue').text)
            return factor,offset
        return None,None

    @classmethod
    def parse_signal_dynamic_behavior(cls,signal):
        dynamic_behaviors_node = signal.find('.//DynamicBehaviors')
        if dynamic_behaviors_node is None:
            return False
        if len(list(dynamic_behaviors_node.iter())) >1:
            # print(len(list(dynamic_behaviors_node.iter())))
            return  True
        return False

    @classmethod
    def parse_signal_definition(cls,signal):
        """
        function used to parese the signal node
        :param signal:
        :return:
        """
        signal_name = signal.get('Name')
        start_bit = signal.find('StartBit').text
        bit_length = signal.find('BitLength').text

        # Initialize a dictionary to store signal information
        signal_info = {
            'Name': signal_name,
            'BitLength': int(bit_length),
        }

        # Check if TableValues node exists
        signal_info['TableValues'] = cls.parse_signal_table_values(signal)
        signal_info['Factor'], signal_info['Offset']  = cls.parse_signal_linear_computation(signal)
        signal_info['Dynamic'] = cls.parse_signal_dynamic_behavior(signal)
        # Check if LinearComputationMethod node exists

        return signal_info

    @classmethod
    def parse_dynamic_container_pdu(cls,pdus_node):
        """
        function used to check if the pdu is a container pdu
        :param pdus_node:
        :return:
        """
        dynamic_container_pdu = pdus_node.find('.//DynamicContainerPduDefinition')
        if dynamic_container_pdu is not None:
            # dlc_dynamic_container_pdu = dynamic_container_pdu.get('Dlc')
            header_dynamic_container_pdu = dynamic_container_pdu.get('Header')
        else:
            header_dynamic_container_pdu = None
        return { 'Header': header_dynamic_container_pdu}

    @classmethod
    def parse_dynamic_pdu_properties(cls, signal_pdu):
        """
        function used to parse dynamic pdu properities
        :param signal_pdu:
        :return:
        """
        dynamic_properties_node = signal_pdu.find('.//DynamicPduProperties')
        if dynamic_properties_node is not None:
            pdu_id = dynamic_properties_node.find('PduId').text
            time_period = dynamic_properties_node.find('TimePeriod').text
        else:
            pdu_id = 0
            time_period = 0
        return {'PduId': pdu_id, 'TimePeriod': time_period}

    @classmethod
    def parse_signal_pdu_definition(cls,signal_pdu):
        signal_pdu_name = signal_pdu.get('Name')
        dlc_signal_pdu = int(signal_pdu.find('Dlc').text)

        # Initialize a dictionary to store Signal PDU information
        signal_pdu_info:dict = {
            'Name': signal_pdu_name,
            'Dlc': dlc_signal_pdu,
        }
        signal_pdu_info["Signals"]:list = []
        dynamic_properties = cls.parse_dynamic_pdu_properties(signal_pdu)
        signal_pdu_info.update(dynamic_properties)
        signals_node = signal_pdu.find('.//Signals')
        if signals_node is not None:
            for signal in signals_node:
                signal_info = cls.parse_signal_definition(signal)
                signal_pdu_info["Signals"].append(signal_info)

        return signal_pdu_info

    @classmethod
    def parse_can_frame_definition(cls,can_frame):
        can_frame_name = can_frame.get('Name')
        dlc_can_frame = can_frame.get('Dlc')

        # Check if Id element exists
        id_can_frame = can_frame.get('Dlc')
        # id_can_frame = id_element.text if id_element is not None else None

        can_frame_info = {
            'Name': can_frame_name,
            'Dlc': int(dlc_can_frame),
            'Id': hex(int(id_can_frame)),
        }
        pdus_node = can_frame.find('.//Pdus')
        if pdus_node is not None:
            pdus_info = []

            dynamic_container_info = cls.parse_dynamic_container_pdu(pdus_node)
            for signal_pdu in pdus_node.findall('.//SignalPduDefinition'):
                signal_pdu_info = cls.parse_signal_pdu_definition(signal_pdu)
                signal_pdu_info.update(dynamic_container_info)
                pdus_info.append(signal_pdu_info)



            can_frame_info["Pdus"] = pdus_info
        return can_frame_info

    @classmethod
    def read_acpdf(cls, file):
        tree = ET.parse(file)
        root = tree.getroot()
        can_frames = root.findall('.//CanFrameDefinition')
        parsed_can_frames = []
        for can_frame in can_frames:
            parsed_can_frame = cls.parse_can_frame_definition(can_frame)
            parsed_can_frames.append(parsed_can_frame)

        # print(parsed_can_frames)
        return parsed_can_frames


    @classmethod
    def flatten_data(cls,parsed_data, output_file='your_existing_file.xlsx'):
        flat_data = []

        for can_frame_info in parsed_data:
            can_frame_dict = {
                'CanFrameName': can_frame_info['Name'],
                'CanFrameDlc': can_frame_info['Dlc'],
                'CanFrameId': can_frame_info.get('Id', None),
            }

            if 'Pdus' in can_frame_info:
                # print(can_frame_info['Pdus'])
                for pdu_info in can_frame_info['Pdus']:
                    pdu_dict = {
                        'PduName': pdu_info['Name'],
                        'PduDlc': pdu_info['Dlc'],
                        'PduId': pdu_info.get('PduId', None),
                        'PduTimePeriod': pdu_info.get('TimePeriod', None),
                        'PduHeader': pdu_info.get('Header', None),
                    }

                    if 'Signals' in pdu_info:
                        for signal_info in pdu_info['Signals']:
                            signal_dict = {
                                'SignalName': signal_info['Name'],
                                'SignalBitLength': signal_info['BitLength'],
                                'SignalTableValues': '\n'.join(signal_info.get('TableValues', [])),
                                'SignalFactor': signal_info.get('Factor', None),
                                'SignalOffset': signal_info.get('Offset', None),
                                 'SignalBehavior':signal_info['Dynamic']
                            }
                            # print({**can_frame_dict, **pdu_dict, **signal_dict})
                            flat_data.append({**can_frame_dict, **pdu_dict, **signal_dict})
                    else:
                        # print()
                        flat_data.append({**can_frame_dict, **pdu_dict})

        df = pd.DataFrame(flat_data)
        df.to_excel(output_file, index=False)



if __name__ == "__main__":
    parsed_can_frames = AcpdfUtil.read_acpdf("test.xml")
    AcpdfUtil.flatten_data(parsed_can_frames)