import pandas as pd

def flatten_data(parsed_data, output_file='output.xlsx'):
    flat_data = []

    for can_frame_info in parsed_data:
        can_frame_dict = {
            'CanFrameName': can_frame_info['Name'],
            'CanFrameDlc': can_frame_info['Dlc'],
            'CanFrameId': can_frame_info.get('Id', None),
        }

        if 'Pdus' in can_frame_info:
            for pdu_info in can_frame_info['Pdus']:
                pdu_dict = {
                    'PduName': pdu_info['Name'],
                    'PduDlc': pdu_info['Dlc'],
                    'PduId': pdu_info.get('PduId', None),
                    'PduTimePeriod': pdu_info.get('TimePeriod', None),
                    'PduHeader': pdu_info.get('Header', None),
                }

                if 'signals' in pdu_info:
                    for signal_info in pdu_info['signals']:
                        signal_dict = {
                            'SignalName': signal_info['Name'],
                            'SignalBitLength': signal_info['BitLength'],
                        }

                        if 'TableValues' in signal_info:
                            signal_dict['SignalTableValues'] = ', '.join(signal_info['TableValues'])
                        else:
                            signal_dict['SignalTableValues'] = None

                        if 'Factor' in signal_info:
                            signal_dict['SignalFactor'] = signal_info['Factor']
                        else:
                            signal_dict['SignalFactor'] = None

                        if 'Offset' in signal_info:
                            signal_dict['SignalOffset'] = signal_info['Offset']
                        else:
                            signal_dict['SignalOffset'] = None

                        flat_data.append({**can_frame_dict, **pdu_dict, **signal_dict})
                else:
                    flat_data.append({**can_frame_dict, **pdu_dict})

    df = pd.DataFrame(flat_data)

    # Save the DataFrame to Excel with openpyxl engine to enable styling
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Access the Excel writer and the default worksheet
        worksheet = writer.sheets['Sheet1']

        # Apply styling options
        for column in worksheet.columns:
            max_length = 0
            column = [column[0].column] + [col.value for col in column]
            for col_index, cell_value in enumerate(column):
                try:
                    if len(str(cell_value)) > max_length:
                        max_length = len(cell_value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0]].width = adjusted_width

        for row in worksheet.iter_rows():
            for cell in row:
                cell.alignment = openpyxl.styles.Alignment(wrap_text=True)

# Assuming parsed_can_frames is the list containing the parsed data
flatten_data(parsed_can_frames)
