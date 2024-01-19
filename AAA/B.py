xml_data = """<Frames>
<CanFrameDefinition Name="ZCUDZCUDCAN1Fr37" Dlc="8" Id="118">
<Transmitter>Aria</Transmitter>
<Receivers>
<string>SRS3</string>
</Receivers>
<Pdus>
<SignalPduDefinition Guid="e066c0c1-904a-4528-9810-13b07e2155ca" Name="ZCUDZCUDCAN1SignalIPDU37" Description="">
<StartBit>0</StartBit>
<Dlc>8</Dlc>
<Endian>Intel</Endian>
<IsEnabled>true</IsEnabled>
<Signals>
<SignalDefinition Name="VehSpdLgtQf">
<Comment>Quality factor for vehicle speed as measured by wheel speed sensors and longitudinal acceleration.</Comment>
<StartBit>42</StartBit>
<BitLength>2</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">1</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="GenQf1_UndefindDataAccur" />
<Item Key="1" KeyType="Ulong" Value="GenQf1_TmpUndefdData" />
<Item Key="2" KeyType="Ulong" Value="GenQf1_DataAccurNotWithinSpcn" />
<Item Key="3" KeyType="Ulong" Value="GenQf1_AccurData" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="VehSpdLgtCntr">
<Comment>Counter</Comment>
<StartBit>44</StartBit>
<BitLength>4</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues />
<DynamicBehaviors>
<CounterSignalBehaviorDefinition Guid="664cf18d-fb03-418c-bebe-b882476f5f48" Name="Counter" Description="">
<Step>1</Step>
<Min>0</Min>
<Max>14</Max>
</CounterSignalBehaviorDefinition>
</DynamicBehaviors>
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="VehSpdLgtChks">
<Comment>Checksum</Comment>
<StartBit>32</StartBit>
<BitLength>8</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues />
<DynamicBehaviors>
<SwCrcSignalBehaviorDefinition Guid="677cbf83-3ee1-4199-8ef1-7556a1b8b4a7" Name="GeelyGEEA3.dll:CalculateCrc" Description="">
<DynamicLibraryIdentity>56f913e8-2d2a-490b-acb6-c1533d18de85</DynamicLibraryIdentity>
<FunctionName>CalculateCrc</FunctionName>
</SwCrcSignalBehaviorDefinition>
</DynamicBehaviors>
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="VehSpdLgtA">
<Comment>Vehicle speed longitudinal based on wheel speed sensors and longitudinal acceleration.</Comment>
<StartBit>24</StartBit>
<BitLength>15</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Double</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<LinearComputationMethod>
<Factor>
<DynamicValue Type="Double">0.00391</DynamicValue>
</Factor>
<Offset>
<DynamicValue Type="Double">0</DynamicValue>
</Offset>
</LinearComputationMethod>
<TableValues />
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="VehSpdLgt_UB">
<Comment />
<StartBit>23</StartBit>
<BitLength>1</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">1</DynamicValue>
</InitialValue>
<TableValues />
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
</Signals>
<UpdateBit>-1</UpdateBit>
</SignalPduDefinition>
</Pdus>
<CustomAttributes />
<Comment />
<ExtendedId>false</ExtendedId>
<IsCanFd>false</IsCanFd>
<Periodicity>20</Periodicity>
</CanFrameDefinition>
<CanFrameDefinition Name="CCP_PTEXTCANFD_PDUGW_FrP03" Dlc="64" Id="434">
<Transmitter />
<Receivers>
<string>SDMCCfg</string>
</Receivers>
<Pdus>
<DynamicContainerPduDefinition Guid="34113c80-a469-4828-b845-d02ddbcf5258" Name="CCP_PTEXTCANFD_020ms_Container03" Description="">
<StartBit>0</StartBit>
<Dlc>64</Dlc>
<Endian>Intel</Endian>
<IsEnabled>true</IsEnabled>
<Pdus>
<SignalPduDefinition Guid="21cda1e3-e357-4a5e-b040-af8b5f70cd64" Name="CCP_020ms_PDU02_PTEXT" Description="">
<StartBit>0</StartBit>
<Dlc>8</Dlc>
<Endian>Intel</Endian>
<IsEnabled>true</IsEnabled>
<DynamicPduProperties>
<PduId>65538</PduId>
<TimePeriod>20</TimePeriod>
<TimeOffset>0</TimeOffset>
</DynamicPduProperties>
<Signals>
<SignalDefinition Name="BPwrMdMstrstrAvlbly">
<Comment>Backup Power Mode Master Availability</Comment>
<StartBit>27</StartBit>
<BitLength>1</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="BPwrMdMstrstrAvlbly_0_FALSE" />
<Item Key="1" KeyType="Ulong" Value="BPwrMdMstrstrAvlbly_1_TRUE" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="CCP_020ms_PDU02_CRC">
<Comment />
<StartBit>0</StartBit>
<BitLength>8</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues />
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="CCP_020ms_PDU02_RC">
<Comment />
<StartBit>8</StartBit>
<BitLength>4</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues />
<DynamicBehaviors>
<CounterSignalBehaviorDefinition Guid="1f2f7a0c-025d-4f0f-a00d-3b646d86677e" Name="Counter" Description="">
<Step>1</Step>
<Min>0</Min>
<Max>14</Max>
</CounterSignalBehaviorDefinition>
</DynamicBehaviors>
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="SysOpnlMd">
<Comment>System Operational Mode</Comment>
<StartBit>13</StartBit>
<BitLength>3</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="SysOpnlMd_0_Normal_Mode" />
<Item Key="1" KeyType="Ulong" Value="SysOpnlMd_1_Manufacturing_Mode" />
<Item Key="2" KeyType="Ulong" Value="SysOpnlMd_2_Transit_Mode" />
<Item Key="3" KeyType="Ulong" Value="SysOpnlMd_3_Show_Room" />
<Item Key="4" KeyType="Ulong" Value="SysOpnlMd_4_Storage_Mode" />
<Item Key="5" KeyType="Ulong" Value="SysOpnlMd_5_Diagnosic_or_Reprogramming_Reserve_" />
<Item Key="6" KeyType="Ulong" Value="SysOpnlMd_6_6_Service_mode" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="SysPwrMd">
<Comment>System Power Mode</Comment>
<StartBit>30</StartBit>
<BitLength>2</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">2</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="SysPwrMd_0_Off" />
<Item Key="1" KeyType="Ulong" Value="SysPwrMd_1_Accessory" />
<Item Key="2" KeyType="Ulong" Value="SysPwrMd_2_Run" />
<Item Key="3" KeyType="Ulong" Value="SysPwrMd_3_CrankRequest" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="SysPwrMdV">
<Comment>System Power Mode Validity</Comment>
<StartBit>26</StartBit>
<BitLength>1</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="SysPwrMdV_0_Valid" />
<Item Key="1" KeyType="Ulong" Value="SysPwrMdV_1_Invalid" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="SysVol">
<Comment>System Voltage</Comment>
<StartBit>16</StartBit>
<BitLength>8</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Double</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<LinearComputationMethod>
<Factor>
<DynamicValue Type="Double">0.1</DynamicValue>
</Factor>
<Offset>
<DynamicValue Type="Double">3</DynamicValue>
</Offset>
</LinearComputationMethod>
<TableValues />
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="SysVolMd">
<Comment>System Voltage Mode</Comment>
<StartBit>28</StartBit>
<BitLength>2</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="SysVolMd_0_Normal" />
<Item Key="1" KeyType="Ulong" Value="SysVolMd_1_LowSystemVoltage" />
<Item Key="2" KeyType="Ulong" Value="SysVolMd_2_HighSystemVoltage" />
<Item Key="3" KeyType="Ulong" Value="SysVolMd_3_IllegalSystemVoltage" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="SysVolMdV">
<Comment>System Voltage Mode Validity</Comment>
<StartBit>12</StartBit>
<BitLength>1</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="SysVolMdV_0_Valid" />
<Item Key="1" KeyType="Ulong" Value="SysVolMdV_1_Invalid" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="SysVolV">
<Comment>System Voltage Validity</Comment>
<StartBit>25</StartBit>
<BitLength>1</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="SysVolV_0_Valid" />
<Item Key="1" KeyType="Ulong" Value="SysVolV_1_Invalid" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="CCP_020ms_PDU02_Reserve02">
<Comment />
<StartBit>56</StartBit>
<BitLength>16</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">415029</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="unknown" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="CCP_020ms_PDU02_Reserve01">
<Comment />
<StartBit>24</StartBit>
<BitLength>1</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">1</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="unknown" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="CCP_020ms_PDU02_Reserve03">
<Comment />
<StartBit>40</StartBit>
<BitLength>8</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">597</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="unknown" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="CCP_020ms_PDU02_Reserve04">
<Comment />
<StartBit>32</StartBit>
<BitLength>5</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">49</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="unknown" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="AccryWkupAndWkupEnbReq">
<Comment>Accessory Wakeup And Wakeup Enable Request</Comment>
<StartBit>37</StartBit>
<BitLength>3</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="AccryWkupAndWkupEnbReq_0_Accessory_Wakeup_And_Wakeup_Enable_Line_Disable" />
<Item Key="1" KeyType="Ulong" Value="AccryWkupAndWkupEnbReq_1_Accessory_Wakeup_And_Wakeup_Enable_Line_Enable" />
<Item Key="2" KeyType="Ulong" Value="AccryWkupAndWkupEnbReq_2_Reserve" />
<Item Key="3" KeyType="Ulong" Value="AccryWkupAndWkupEnbReq_3_Reserve" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
</Signals>
<UpdateBit>-1</UpdateBit>
</SignalPduDefinition>
<SignalPduDefinition Guid="ad1cf4f6-a2b4-4500-9cef-5de8b44e31aa" Name="FVCM_020ms_PDU02_SGWPTEXT" Description="">
<StartBit>0</StartBit>
<Dlc>8</Dlc>
<Endian>Intel</Endian>
<IsEnabled>true</IsEnabled>
<DynamicPduProperties>
<PduId>133378</PduId>
<TimePeriod>20</TimePeriod>
<TimeOffset>0</TimeOffset>
</DynamicPduProperties>
<Signals>
<SignalDefinition Name="HandOffStrgWhlDetnSta">
<Comment>Hand Off Steering Wheel Detection State</Comment>
<StartBit>12</StartBit>
<BitLength>2</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">1</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="HandOffStrgWhlDetnSta_0_HandsOff_level1_" />
<Item Key="1" KeyType="Ulong" Value="HandOffStrgWhlDetnSta_1_HandsOn" />
<Item Key="2" KeyType="Ulong" Value="HandOffStrgWhlDetnSta_2_HandsOff_level2_" />
<Item Key="3" KeyType="Ulong" Value="HandOffStrgWhlDetnSta_3_HandsOff_level3_" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="TJAICASysFltSts">
<Comment>Traffic Jam Assist Integrated Cruise Assist Fault Status</Comment>
<StartBit>2</StartBit>
<BitLength>3</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="TJAICASysFltSts_0_noerror" />
<Item Key="1" KeyType="Ulong" Value="TJAICASysFltSts_1_performancedegradation" />
<Item Key="2" KeyType="Ulong" Value="TJAICASysFltSts_2_systemtemporaryunavailable" />
<Item Key="3" KeyType="Ulong" Value="TJAICASysFltSts_3_servicerequired" />
<Item Key="4" KeyType="Ulong" Value="TJAICASysFltSts_4_ALC_Fault" />
<Item Key="5" KeyType="Ulong" Value="TJAICASysFltSts_5_Reserved" />
<Item Key="6" KeyType="Ulong" Value="TJAICASysFltSts_6_Reserved" />
<Item Key="7" KeyType="Ulong" Value="TJAICASysFltSts_7_Reserved" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
<SignalDefinition Name="TJAICASysSts">
<Comment>Traffic Jam Assist Integrated Cruise Assist System Status</Comment>
<StartBit>5</StartBit>
<BitLength>3</BitLength>
<UpdateBitPosition>-1</UpdateBitPosition>
<Endian>Motorola</Endian>
<Unit />
<RawValueType>Ulong</RawValueType>
<PhysicalValueType>Ulong</PhysicalValueType>
<InitialValue>
<DynamicValue Type="Ulong">0</DynamicValue>
</InitialValue>
<TableValues>
<Item Key="0" KeyType="Ulong" Value="TJAICASysSts_0_Off" />
<Item Key="1" KeyType="Ulong" Value="TJAICASysSts_1_Standby" />
<Item Key="2" KeyType="Ulong" Value="TJAICASysSts_2_Active" />
<Item Key="3" KeyType="Ulong" Value="TJAICASysSts_3_Override" />
<Item Key="4" KeyType="Ulong" Value="TJAICASysSts_4_Passive" />
<Item Key="5" KeyType="Ulong" Value="TJAICASysSts_5_reserved" />
<Item Key="6" KeyType="Ulong" Value="TJAICASysSts_6_reserved" />
<Item Key="7" KeyType="Ulong" Value="TJAICASysSts_7_reserved" />
</TableValues>
<DynamicBehaviors />
<CustomAttributes />
</SignalDefinition>
</Signals>
<UpdateBit>-1</UpdateBit>
</SignalPduDefinition>
</Pdus>
<Header>Short</Header>
<Timeout>0</Timeout>
</DynamicContainerPduDefinition>
</Pdus>
<CustomAttributes />
<Comment />
<ExtendedId>false</ExtendedId>
<IsCanFd>true</IsCanFd>
<Periodicity>0</Periodicity>
</CanFrameDefinition>
</Frames>"""
