import copy
import re
from datetime import datetime
from typing import Generator, Tuple, cast, Any, Dict, List, Union
import struct
import datetime
import zlib
import re
from abc import ABC, abstractmethod
import uds
import udsoncan

# TODO合并 log类里面的函数，并优化
def dlc2len(dlc: int) -> int:
    """Calculate the data length from DLC.

    :param dlc: DLC (0-15)

    :returns: Data length in number of bytes (0-64)
    """
    return CAN_FD_DLC[dlc] if dlc <= 15 else 64


CAN_FD_DLC = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64]

TSystemTime = Tuple[int, int, int, int, int, int, int, int]


def systemtime_to_timestamp(systemtime) -> float:
    try:
        t = datetime.datetime(
            systemtime[0],
            systemtime[1],
            systemtime[3],
            systemtime[4],
            systemtime[5],
            systemtime[6],
            systemtime[7] * 1000,
        )
        return t.timestamp()
    except ValueError:
        return 0


class FRAME_DIRECTION:
    RX: int = 0
    TX: int = 1
    BOTH: int = 2


class LOG_FILTERING:
    INCLUSION: int = 0
    EXCLUSION: int = 1


class EVENT_TYPE:
    GENERAL: int = 1
    CAN_ERROR: int = 2

    LIN_SLEEP: int = 3
    LIN_WAKEUP: int = 4
    LIN_NOANSWER: int = 5
    LIN_ERROR: int = 6
    LIN_SYNCERROR: int = 7
    FLEXRAY_START_CYCLE: int = 8
    FLEXRAY_STATUS: int = 9
    FLEXRAY_WAKEUP: int = 10
    FLEXRAY_SPY: int = 11
    FLEXRAY_SYMBOL_WINDOW: int = 12
    FLEXRAY_NM_VECTOR: int = 13
    FLEXRAY_TRANCEIVER_STATUS: int = 14
    FLEXRAY_SPY_SYMBOL: int = 15
    FLEXRAY_INVALID: int = 16
    FLEXRAY_ERROR: int = 17


class BUS_PROTOCOL:
    ERROR: str = "ErrorFrame"
    UNKNOWN: str = "Unknown"
    CAN: str = "CAN"
    CANFD: str = "CANFD"
    FLEXRAY: str = "Flexray"


class LogEventData(ABC):
    """
    Base frame type. Must be check typed for further processing.
    """

    def __init__(self, timestamp: float = 0.0, channel: int = 0) -> None:
        self.timestamp: float = timestamp  # the unit shall be ms,
        self.channel: int = channel
        self.protocol: BUS_PROTOCOL = BUS_PROTOCOL.UNKNOWN

    def __str__(self) -> str:
        frame_strs = (
            f"Timestamp: {self.timestamp}\t"
            f"Channel: {self.channel}\t "
            f"protocol: {self.protocol}\t "
        )
        return frame_strs


class LogErrorFrame(LogEventData):

    def __init__(self, timestamp: float = 0.0, channel: int = 0, message: str = ""):
        super().__init__(timestamp, channel)
        self.message: str = message
        # self.type:EVENT_TYPE = EVENT_TYPE.CAN_ERROR

    def __str__(self) -> str:
        frame_strs = (
            f"Timestamp: {self.timestamp}\t"
            f"Channel: {self.channel}\t "
            f"Message: {self.message}\t "
        )
        return frame_strs


class LogRemoteFrame(LogEventData):
    # TODO currently no remote frame, will not use it
    def __init__(self, timestamp: float = 0.0, channel: int = 0, message: str = ""):
        super.__init__(timestamp, channel)
        self.message: str = message
        self.type: EVENT_TYPE = EVENT_TYPE.CAN_ERROR

    def __str__(self) -> str:
        frame_strs = (
            f"Timestamp: {self.timestamp}\t"
            f"Channel: {self.channel}\t "
            f"Message: {self.message}\t "
            f"Type: {self.type}\t "
        )
        return frame_strs


class LogCanFrame(LogEventData):

    def __init__(self, timestamp: float, channel: int, id: int, direction: FRAME_DIRECTION, dlc: int,
                 payload: bytearray):
        self.timestamp: float = timestamp
        self.period:float = 0.0
        self.channel: int = channel
        self.id: int = id
        self.direction: FRAME_DIRECTION = direction
        self.dlc: int = dlc
        self.payload: bytearray = payload

    def __str__(self) -> str:
        frame_strs = (
            f"Timestamp: {self.timestamp}\t"
            f"Period: {self.period}\t"
            f"Channel: {self.channel}\t "
            f"ID: {self.id}\t "
            f"Direction: {self.direction}\t "
            f"DLC: {self.dlc}\t "
            f"Payload:{self.payload.hex(' ')}"
        )
        return frame_strs


class LogFlexFrame(LogEventData):

    def __init__(self, timestamp: float = 0,
                 channel: int = 0,
                 direction: FRAME_DIRECTION = FRAME_DIRECTION.TX,
                 slot: int = 0,
                 cycle: int = 0,
                 dlc: int = 0,
                 payload: bytearray = None
                 ) -> None:
        super().__init__(timestamp, channel)
        self.direction: FRAME_DIRECTION = direction
        self.slot: int = slot
        self.cycle: int = cycle
        self.dlc: int = dlc
        self.payload: bytearray = payload

    def __str__(self) -> str:
        frame_strs = (
            f"Timestamp: {self.timestamp}\t"
            f"Channel: {self.channel}\t "
            f"Direction: {self.direction}\t "
            f"Slot: {self.slot}\t "
            f"Cycle: {self.cycle}\t "
            f"DLC: {self.dlc}\t "
            f"Payload:{self.payload.hex(' ')}"
        )
        return frame_strs


class AriaLegacyLog:
    CanLogEntryDirectionIndex = 0
    CanLogEntryChannelIndex = 1
    CanLogEntryTimestampIndex = 2
    CanLogEntryFrameIdIndex = 3
    CanLogEntryFrameDLC = 4
    CanLogEntryPayloadStartIndex = 5
    CanLogEntryMinPropertiesNo = 6

    def __init__(self, file: str):
        self.io = open(file, 'r')

    def __iter__(self):
        for line in self.io:
            LogCanFrame = self._read_can_frame(line)
            # TODO Read Other KIND Frame
            if LogCanFrame is not None:
                yield LogCanFrame
            else:
                continue
        self.io.close()

    def _read_can_frame(self, line: str):
        """function used to

        Args:
            line (str): _description_

        Returns:
            _type_: _description_
        """
        frameProps = line.split(",")

        if len(frameProps) < self.CanLogEntryMinPropertiesNo:  # the array legnth is not enough
            return None

        # channel
        strChannel = frameProps[self.CanLogEntryChannelIndex]
        match = re.match(r".*?(\d+)$", strChannel)
        if match:
            channel = int(match.group(1))
        else:
            channel = None
        # timestamp
        strTimeStamp = frameProps[self.CanLogEntryTimestampIndex].replace("t=", "")
        try:
            timestamp = float(strTimeStamp)
        except:
            timestamp = None

        strDirection = frameProps[self.CanLogEntryDirectionIndex].upper()
        # direction
        if strDirection == "TX_MSG":
            direction = FRAME_DIRECTION.TX
        elif strDirection == "RX_MSG":
            direction = FRAME_DIRECTION.RX
        elif strDirection == "ERR_MSG":  # TODO，python的。log和js里面的格式有差异
            return LogErrorFrame(timestamp, channel, line)
        else:
            direction = None

        strID = frameProps[self.CanLogEntryFrameIdIndex].replace("id=", "")
        try:
            id = int(strID, 16)
        except Exception as err:
            id = None

        strDlc = frameProps[self.CanLogEntryFrameDLC].replace("l=", "")
        try:
            dlc = int(strDlc)
        except:
            dlc = None

        payload = bytearray.fromhex(frameProps[self.CanLogEntryPayloadStartIndex])
        # print([direction,channel,timestamp,id,dlc])
        if None in [direction, channel, timestamp, id, dlc]:
            return None
        else:
            return LogCanFrame(timestamp, channel, id, direction, dlc, payload)


class VectorAscLog:

    def __init__(self, file):
        self.io = open(file, 'r')

        self._parse_asc_header()
        self.base = self.header_info['base']
        self.timestamps_format = self.header_info["timestamps_format"]
        self.start_time = self._convert_asc_date_to_datetime(self.header_info["date"])

    def _parse_can_id(self, strId: str) -> int:
        """function used to parse can id from the string,
        the format have two kind type:
        18EBFF00x:extened id
        6F9:normal
        Args:
            strId (str): _description_

        Returns:
            _type_: _description_
        """
        if strId.endswith("x"):  # extenedid
            return int(strId[:-1], self.base)
        else:
            return int(strId, self.base)

    def _convert_asc_date_to_datetime(self, asc_date_str) -> Union[datetime.datetime, None]:
        """_a function used to conver the date to timestamp
           in the header, the format as below "date Thu Apr 28 10:44:52.480 am 2022"

        Args:
            asc_date_str (_type_): _Thu Apr 28 10:44:52.480 am 2022_

        Returns:
            _type_: _description_
        """
        try:
            # You may need to adjust the format based on the actual date format in your ASC log
            datetime_obj = datetime.datetime.strptime(asc_date_str, "%a %b %d %I:%M:%S %p %Y")
            return datetime_obj
        except ValueError as e:
            print(f"Error converting ASC date to datetime: {e}")
            return None

    def _parse_asc_header(self):
        """_parse the header info
        below is an example of header
        # date Wed Aug 09 01:27:06 AM 2023
        # base dec timestamps relative
            #dec or hex
            # `relative` (starting at 0.0) or `absolute` (starting at the system time)
        # internal events logged
        # // version x.0.0
        # Begin Triggerblock Thu Jan 01 04:34:18 PM 1970
        """
        self.header_info = {"date": None, 'base': None, "timestamps_format": None}
        for line in self.io:
            line = line.strip()
            if line.startswith('date '):
                self.header_info['date'] = line.split(" ")[1].strip()

            elif line.startswith('base '):
                temp = line.split(" ")
                # TODO temp[1] must hex or dec
                self.header_info['base'] = 16 if temp[1] == "hex" else 10
                self.header_info['timestamps_format'] = temp[3]
            if line.startswith("Begin"):
                break

    def _read_can_frame(self, line: str, temp: List[str]):
        channel = int(temp[1])
        timestamp = float(temp[0]) * 1000  # TODO 是否加上开始时间
        if line.find("ErrorFrame") > 0:
            return LogErrorFrame(timestamp, channel, line[line.find("ErrorFrame"):])
        else:
            strId = temp[2]
            strDirection = temp[3].upper()

            # 处理Direction
            if strDirection == "TX":
                direction = FRAME_DIRECTION.TX
            elif strDirection == "RX":
                direction = FRAME_DIRECTION.RX
            else:
                return None
            id = self._parse_can_id(strId)

            if temp[4].upper() == "R":  # remote LogCanFrame
                return None
            else:
                strDlc = temp[5]
                dlc = int(strDlc, self.base)
                payload: bytearray = bytearray()
                for byte in temp[6:6 + dlc]:
                    payload.append(int(byte, self.base))
                return LogCanFrame(timestamp, channel, id, direction, dlc, payload)

    def _read_can_fd_frame(self, line: str, temp: List[str]):
        timestamp = float(temp[0]) * 1000  # TODO 是否加上开始时间
        channel = int(temp[2])
        strDirection = temp[3].upper()
        # print(strDirection)
        # 处理Direction
        if strDirection == "TX":
            direction = FRAME_DIRECTION.TX
        elif strDirection == "RX":
            direction = FRAME_DIRECTION.RX
        else:
            return None

        if line.find("ErrorFrame") > 0:
            # print(line)
            return LogErrorFrame(timestamp, channel, line[line.find("ErrorFrame"):])
        else:
            strId = temp[4]
            id = self._parse_can_id(strId)
            frame_name_or_brs = temp[5]

            if frame_name_or_brs.isdigit():
                brs = frame_name_or_brs
                esi = temp[6]
                strDlc = temp[7]  # 1-8 CANFD DLC
                data_length = temp[8]  # payload DLC
                dlc = int(data_length)
                # data_length = int(data_length)
                if dlc == 0:  # remote LogCanFrame
                    return None
                payload: bytearray = bytearray()
                for byte in temp[9:9 + dlc]:
                    payload.append(int(byte, self.base))

            else:
                brs = temp[6]
                esi = temp[7]
                strDlc = temp[8]
                data_length = temp[9]
                dlc = int(data_length)
                data_length = int(data_length)
                if dlc == 0:  # remote LogCanFrame
                    return None
                payload: bytearray = bytearray()
                for byte in temp[10:10 + dlc]:
                    payload.append(int(byte, self.base))
            return LogCanFrame(timestamp, channel, id, direction, dlc, payload)


    def _read_frame(self, line: str):
        line = line.strip()
        try:
            temp: List[str] = line.split()
            if temp[1] == "CANFD":
                return self._read_can_fd_frame(line, temp)
            elif temp[1].isdigit():
                return self._read_can_frame(line, temp)
        except:
            pass
        return None

    def __iter__(self):
        for line in self.io:
            frame = self._read_frame(line)
            if frame is not None:
                yield frame
            else:
                continue
        self.io.close()


class BlfHeaderStruct:
    STRUCT = struct.Struct("<4sLBBBBBBBBQQLL8H8H")
    SIZE = 144

    def __init__(self, data):
        self.fields = self.STRUCT.unpack(data)
        self.signature = self.fields[0]
        self.header_size = self.fields[1]
        # self.app_id = self.fields[2]
        # self.app_major = self.fields[3]
        # self.app_minor = self.fields[4]
        # self.app_build = self.fields[5]
        # self.bin_log_major =  self.fields[6]
        # self.bin_log_minor = self.fields[7]
        # self.bin_log_build = self.fields[8]
        # self.bin_log_patch = self.fields[9]
        self.file_size = self.fields[10]
        self.uncompressed_size = self.fields[11]
        self.obj_count = self.fields[12]
        self.obj_count_read = self.fields[13]
        self.start_timestamp = self.fields[14:22]
        self.stop_timestamp = self.fields[22:30]
        print(self.start_timestamp, self.fields[14:22], self.fields[22:30])


class ObjHeaderBaseStruct:
    STRUCT = struct.Struct("<4sHHLL")

    def __init__(self, data, pos: int = 0):
        self.signature, \
        self.header_size, \
        self.header_version, \
        self.obj_size, \
        self.obj_type = self.STRUCT.unpack_from(data, pos)


class ObjHeaderV1Struct:
    STRUCT = struct.Struct("<LHHQ")

    def __init__(self, data, pos: int = 0):
        self.flags, \
        self.client_index, \
        self.obj_version, \
        self.timestamp = self.STRUCT.unpack_from(data, pos)


class ObjHeaderV2Struct:
    STRUCT = struct.Struct("<LBxHQ8x")

    def __init__(self, data, pos: int = 0):
        self.flags, \
        self.timestamp_status, \
        self.obj_version, \
        self.timestamp = self.STRUCT.unpack_from(data, pos)


class LogContainerStruct:
    STRUCT = struct.Struct("<H6xL4x")

    def __init__(self, data, pos: int = 0):
        self.compression_method, \
        self.uncompressed_size = self.STRUCT.unpack_from(data, pos)


class CanFrameStruct:
    STRUCT = struct.Struct("<HBBL8s")

    def __init__(self, data, pos: int = 0):
        self.channel, \
        self.flags, \
        self.dlc, \
        self.arbitration_id, \
        self.data = self.STRUCT.unpack_from(data, pos)


class CanFdFrameStruct:
    STRUCT = struct.Struct("<HBBLLBBB5x64s")

    def __init__(self, data, pos: int = 0):
        self.channel, \
        self.flags, \
        self.dlc, \
        self.arbitration_id, \
        _, \
        _, \
        self.fd_flags, \
        self.valid_bytes, \
        self.data = self.STRUCT.unpack_from(data, pos)


class CanFdFrame64Struct:
    STRUCT = struct.Struct("<BBBBLLLLLLLHBBL")

    def __init__(self, data, pos: int = 0):
        self.channel, \
        self.dlc, \
        self.valid_bytes, \
        _, \
        self.arbitration_id, \
        _, \
        self.fd_flags, \
        _, \
        _, \
        _, \
        _, \
        _, \
        self.direction, \
        _, \
        _, = self.STRUCT.unpack_from(data, pos)


class CanErrorExtStruct:
    STRUCT = struct.Struct("<HHLBBBxLLH2x8s")

    def __init__(self, data, pos: int = 0):
        self.channel, \
        self.dlc, \
        self.valid_payload_length, \
        _, \
        self.arbitration_id, \
        _, \
        self.fd_flags, \
        _, \
        _, \
        _, \
        _, \
        _, \
        _, \
        self.ecc, \
        self.position, \
        self.data = self.STRUCT.unpack_from(data, pos)


class BlfEvent:
    EDL = 0x1
    BRS = 0x2
    ESI = 0x4
    DIR = 0x1
    ZLIB_DEFLATE = 2
    NO_COMPRESSION = 0
    UNKNOWN = 0  # . /**< unknown object */
    CAN_FRAME = 1  # . /**< CAN message object */
    CAN_ERROR = 2  # . /**< CAN error frame object */
    CAN_OVERLOAD = 3  # . /**< CAN overload frame object */
    CAN_STATISTIC = 4  # . /**< CAN driver statistics object */
    APP_TRIGGER = 5  # . /**< application trigger object */
    ENV_INTEGER = 6  # . /**< environment integer object */
    ENV_DOUBLE = 7  # . /**< environment double object */
    ENV_STRING = 8  # . /**< environment string object */
    ENV_DATA = 9  # . /**< environment data object */
    LOG_CONTAINER = 10  # . /**< container object */
    LIN_MESSAGE = 11  # . /**< LIN message object */
    LIN_CRC_ERROR = 12  # . /**< LIN CRC error object */
    LIN_DLC_INFO = 13  # . /**< LIN DLC info object */
    LIN_RCV_ERROR = 14  # . /**< LIN receive error object */
    LIN_SND_ERROR = 15  # . /**< LIN send error object */
    LIN_SLV_TIMEOUT = 16  # . /**< LIN slave timeout object */
    LIN_SCHED_MODCH = 17  # . /**< LIN scheduler mode change object */
    LIN_SYN_ERROR = 18  # . /**< LIN sync error object */
    LIN_BAUDRATE = 19  # . /**< LIN baudrate event object */
    LIN_SLEEP = 20  # . /**< LIN sleep mode event object */
    LIN_WAKEUP = 21  # . /**< LIN wakeup event object */
    MOST_SPY = 22  # . /**< MOST spy message object */
    MOST_CTRL = 23  # . /**< MOST control message object */
    MOST_LIGHTLOCK = 24  # . /**< MOST light lock object */
    MOST_STATISTIC = 25  # . /**< MOST statistic object */
    Reserved26 = 26  # . /**< reserved */
    Reserved27 = 27  # . /**< reserved */
    Reserved28 = 28  # . /**< reserved */
    FLEXRAY_DATA = 29  # . /**< FLEXRAY data object */
    FLEXRAY_SYNC = 30  # . /**< FLEXRAY sync object */
    CAN_DRIVER_ERROR = 31  # . /**< CAN driver error object */
    MOST_PKT = 32  # . /**< MOST Packet */
    MOST_PKT2 = 33  # . /**< MOST Packet including original timestamp */
    MOST_HWMODE = 34  # . /**< MOST hardware mode event */
    MOST_REG = 35  # . /**< MOST register data (various chips) */
    MOST_GENREG = 36  # . /**< MOST register data (MOST register) */
    MOST_NETSTATE = 37  # . /**< MOST NetState event */
    MOST_DATALOST = 38  # . /**< MOST data lost */
    MOST_TRIGGER = 39  # . /**< MOST trigger */
    FLEXRAY_CYCLE = 40  # . /**< FLEXRAY V6 start cycle object */
    FLEXRAY_MESSAGE = 41  # . /**< FLEXRAY V6 message object */
    LIN_CHECKSUM_INFO = 42  # . /**< LIN checksum info event object */
    LIN_SPIKE_EVENT = 43  # . /**< LIN spike event object */
    CAN_DRIVER_SYNC = 44  # . /**< CAN driver hardware sync */
    FLEXRAY_STATUS = 45  # . /**< FLEXRAY status event object */
    GPS_EVENT = 46  # . /**< GPS event object */
    FR_ERROR = 47  # . /**< FLEXRAY error event object */
    FR_STATUS = 48  # . /**< FLEXRAY status event object */
    FR_STARTCYCLE = 49  # . /**< FLEXRAY start cycle event object */
    FR_RCVMESSAGE = 50  # . /**< FLEXRAY receive message event object */
    REALTIMECLOCK = 51  # . /**< Realtime clock object */
    Reserved52 = 52  # . /**< this object ID is available for the future */
    Reserved53 = 53  # . /**< this object ID is available for the future */
    LIN_STATISTIC = 54  # . /**< LIN statistic event object */
    J1708_MESSAGE = 55  # . /**< J1708 message object */
    J1708_VIRTUAL_MSG = 56  # . /**< J1708 message object with more than 21 data bytes */
    LIN_MESSAGE2 = 57  # . /**< LIN frame object - extended */
    LIN_SND_ERROR2 = 58  # . /**< LIN transmission error object - extended */
    LIN_SYN_ERROR2 = 59  # . /**< LIN sync error object - extended */
    LIN_CRC_ERROR2 = 60  # . /**< LIN checksum error object - extended */
    LIN_RCV_ERROR2 = 61  # . /**< LIN receive error object */
    LIN_WAKEUP2 = 62  # . /**< LIN wakeup event object  - extended */
    LIN_SPIKE_EVENT2 = 63  # . /**< LIN spike event object - extended */
    LIN_LONG_DOM_SIG = 64  # . /**< LIN long dominant signal object */
    APP_TEXT = 65  # . /**< text object */
    FR_RCVMESSAGE_EX = 66  # . /**< FLEXRAY receive message ex event object */
    MOST_STATISTICEX = 67  # . /**< MOST extended statistic event */
    MOST_TXLIGHT = 68  # . /**< MOST TxLight event */
    MOST_ALLOCTAB = 69  # . /**< MOST Allocation table event */
    MOST_STRESS = 70  # . /**< MOST Stress event */
    ETHERNET_FRAME = 71  # . /**< Ethernet frame object */
    SYS_VARIABLE = 72  # . /**< system variable object */
    CAN_ERROR_EXT = 73  # . /**< CAN error frame object (extended) */
    CAN_DRIVER_ERROR_EXT = 74  # . /**< CAN driver error object (extended) */
    LIN_LONG_DOM_SIG2 = 75  # . /**< LIN long dominant signal object - extended */
    MOST_150_MESSAGE = 76  # . /**< MOST150 Control channel message */
    MOST_150_PKT = 77  # . /**< MOST150 Asynchronous channel message */
    MOST_ETHERNET_PKT = 78  # . /**< MOST Ethernet channel message */
    MOST_150_MESSAGE_FRAGMENT = 79  # . /**< Partial transmitted MOST50/150 Control channel message */
    MOST_150_PKT_FRAGMENT = 80  # . /**< Partial transmitted MOST50/150 data packet on asynchronous channel */
    MOST_ETHERNET_PKT_FRAGMENT = 81  # . /**< Partial transmitted MOST Ethernet packet on asynchronous channel */
    MOST_SYSTEM_EVENT = 82  # . /**< Event for various system states on MOST */
    MOST_150_ALLOCTAB = 83  # . /**< MOST50/150 Allocation table event */
    MOST_50_MESSAGE = 84  # . /**< MOST50 Control channel message */
    MOST_50_PKT = 85  # . /**< MOST50 Asynchronous channel message */
    CAN_FRAME_2 = 86  # . /**< CAN message object - extended */
    LIN_UNEXPECTED_WAKEUP = 87  # .
    LIN_SHORT_OR_SLOW_RESPONSE = 88  # .
    LIN_DISTURBANCE_EVENT = 89  # .
    SERIAL_EVENT = 90  # .
    OVERRUN_ERROR = 91  # . /**< driver overrun event */
    EVENT_COMMENT = 92  # .
    WLAN_FRAME = 93  # .
    WLAN_STATISTIC = 94  # .
    MOST_ECL = 95  # . /**< MOST Electrical Control Line event */
    GLOBAL_MARKER = 96  # .
    AFDX_FRAME = 97  # .
    AFDX_STATISTIC = 98  # .
    KLINE_STATUSEVENT = 99  # . /**< E.g. wake-up pattern */
    CAN_FD_FRAME = 100  # . /**< CAN FD message object */
    CAN_FD_FRAME_64 = 101  # . /**< CAN FD message object */
    ETHERNET_RX_ERROR = 102  # . /**< Ethernet RX error object */
    ETHERNET_STATUS = 103  # . /**< Ethernet status object */
    CAN_FD_ERROR_64 = 104  # . /**< CAN FD Error Frame object */
    LIN_SHORT_OR_SLOW_RESPONSE2 = 105  # .
    AFDX_STATUS = 106  # . /**< AFDX status object */
    AFDX_BUS_STATISTIC = 107  # . /**< AFDX line-dependent busstatistic object */
    Reserved108 = 108  # .
    AFDX_ERROR_EVENT = 109  # . /**< AFDX asynchronous error event */
    A429_ERROR = 110  # . /**< A429 error object */
    A429_STATUS = 111  # . /**< A429 status object */
    A429_BUS_STATISTIC = 112  # . /**< A429 busstatistic object */
    A429_MESSAGE = 113  # . /**< A429 Message */
    ETHERNET_STATISTIC = 114  # . /**< Ethernet statistic object */
    Unknown115 = 115  # .
    Reserved116 = 116  # .
    Reserved117 = 117  # .
    TEST_STRUCTURE = 118  # . /**< Event for test execution flow */
    DIAG_REQUEST_INTERPRETATION = 119  # . /**< Event for correct interpretation of diagnostic requests */
    ETHERNET_FRAME_EX = 120  # . /**< Ethernet packet extended object */
    ETHERNET_FRAME_FORWARDED = 121  # . /**< Ethernet packet forwarded object */
    ETHERNET_ERROR_EX = 122  # . /**< Ethernet error extended object */
    ETHERNET_ERROR_FORWARDED = 123  # . /**< Ethernet error forwarded object */
    FUNCTION_BUS = 124  # . /**< FunctionBus object */
    DATA_LOST_BEGIN = 125  # . /**< Data lost begin */
    DATA_LOST_END = 126  # . /**< Data lost end */
    WATER_MARK_EVENT = 127  # . /**< Watermark event */
    TRIGGER_CONDITION = 128  # . /**< Trigger Condition event */
    CAN_SETTING_CHANGED = 129  # . /**< CAN Settings Changed object */
    DISTRIBUTED_OBJECT_MEMBER = 130  # . /**< Distributed object member (communication setup) */
    ATTRIBUTE_EVENT = 131  # . /**< ATTRIBUTE event (communication setup) */


class VectorBlfLog:

    def __init__(self, file: str):
        self.io = open(file, "rb")

        self._parse_header()
        self.start_timestamp = systemtime_to_timestamp(self.blf_header.start_timestamp)
        self.stop_timestamp = systemtime_to_timestamp(self.blf_header.start_timestamp)
        self._tail = b""
        self._pos = 0

    def _parse_header(self):

        self.blf_header: BlfHeaderStruct = BlfHeaderStruct(self.io.read(BlfHeaderStruct.STRUCT.size))
        if self.blf_header.signature != b"LOGG":
            raise Exception("Unexpected file format")
        # Read rest of header
        self.io.read(self.blf_header.header_size - BlfHeaderStruct.STRUCT.size)

    def __iter__(self) -> Generator[LogErrorFrame, LogCanFrame, None]:
        while True:
            data = self.io.read(ObjHeaderBaseStruct.STRUCT.size)
            if not data:
                # EOF
                break

            data = self._check_log_type(data)
            if data is None:
                continue
            else:
                yield from self._parse_container(data)
        self.io.close()

    def _check_log_type(self, data: str):
        obj_header: ObjHeaderBaseStruct = ObjHeaderBaseStruct(data)
        if obj_header.signature != b"LOBJ":
            raise Exception()
        obj_data = self.io.read(obj_header.obj_size - ObjHeaderBaseStruct.STRUCT.size)
        self.io.read(obj_header.obj_size % 4)

        if obj_header.obj_type == BlfEvent.LOG_CONTAINER:
            log_continer = LogContainerStruct(obj_data)
            container_data = obj_data[LogContainerStruct.STRUCT.size:]
            if log_continer.compression_method == BlfEvent.NO_COMPRESSION:
                return container_data
            elif log_continer.compression_method == BlfEvent.ZLIB_DEFLATE:
                data = zlib.decompress(container_data, 15, log_continer.uncompressed_size)
                return data
            else:
                pass
        return None

    def _parse_container(self, data: str):
        if self._tail:
            data = b"".join((self._tail, data))
        try:
            yield from self._read_frame(data)
        except struct.error:
            # There was not enough data in the container to unpack a struct
            pass
        # Save the remaining data that could not be processed
        self._tail = data[self._pos:]

    def _read_can_frame(self, timestamp: float, data: bytes, pos: int):
        channel, flags, dlc, can_id, can_data = CanFrameStruct.STRUCT.unpack_from(data, pos)
        is_rx = not bool(flags & BlfEvent.DIR)
        direction = FRAME_DIRECTION.RX if is_rx else FRAME_DIRECTION.TX
        return LogCanFrame(timestamp, channel, can_id, direction, dlc, bytearray(can_data[:dlc]))

    def _read_error_frame(self, timestamp: float, data: bytes, pos: int):
        members = CanErrorExtStruct.STRUCT.unpack_from(data, pos)
        channel = members[0]
        dlc = members[5]
        can_id = members[7]
        can_data: bytes = members[9]
        return LogErrorFrame(timestamp, channel, can_data[:dlc].hex())

    def _read_can_fd_frame(self, timestamp: float, data: bytes, pos: int):
        members = CanFdFrameStruct.STRUCT.unpack_from(data, pos)
        (
            channel,
            flags,
            dlc,
            can_id,
            _,
            _,
            fd_flags,
            valid_bytes,
            can_data,
        ) = members

        is_rx = not bool(flags & BlfEvent.DIR)
        dlc = dlc2len(dlc)
        direction = FRAME_DIRECTION.RX if is_rx else FRAME_DIRECTION.TX
        return LogCanFrame(timestamp, channel, can_id, direction, dlc, bytearray(can_data[:valid_bytes]))

    def _read_can_fd_frame_64(self, timestamp: float, data: bytes, pos: int):
        (
            channel,
            dlc,
            valid_bytes,
            _,
            can_id,
            _,
            fd_flags,
            _,
            _,
            _,
            _,
            _,
            direction,
            _,
            _,
        ) = CanFdFrame64Struct.STRUCT.unpack_from(data, pos)
        pos += CanFdFrame64Struct.STRUCT.size
        is_rx = not direction
        dlc = dlc2len(dlc)
        direction = FRAME_DIRECTION.RX if is_rx else FRAME_DIRECTION.TX
        return LogCanFrame(timestamp, channel, can_id, direction, dlc, bytearray(data[pos: pos + valid_bytes]))

    def _read_frame(self, data: str):
        start_timestamp = self.start_timestamp
        max_pos = len(data)
        pos = 0
        # Loop until a struct unpack raises an exception
        while True:
            self._pos = pos
            # Find next object after padding (depends on object type)
            try:
                pos = data.index(b"LOBJ", pos, pos + 8)
            except ValueError:
                if pos + 8 > max_pos:
                    # Not enough data in container
                    return
                raise Exception("Could not find next object") from None
            obj_header: ObjHeaderBaseStruct = ObjHeaderBaseStruct(data, pos)
            if obj_header.signature != b"LOBJ":
                raise Exception()
            # Calculate position of next object
            next_pos = pos + obj_header.obj_size
            if next_pos > max_pos:
                # This object continues in the next container
                return
            pos += ObjHeaderBaseStruct.STRUCT.size
            # Read rest of header
            if obj_header.header_version == 1:
                obj_header_v = ObjHeaderV1Struct(data, pos)
                pos += ObjHeaderV1Struct.STRUCT.size
            elif obj_header.header_version == 2:
                obj_header_v = ObjHeaderV2Struct(data, pos)
                pos += ObjHeaderV2Struct.STRUCT.size
            else:
                # TODO, failure infomation
                pos = next_pos
                continue

            # Calculate absolute timestamp in seconds
            factor = 1e-5 if obj_header_v.flags == 1 else 1e-9
            timestamp = (obj_header_v.timestamp * factor + start_timestamp) * 1000
            # TODO 时间需要保持一致ms
            if obj_header.obj_type in (BlfEvent.CAN_FRAME, BlfEvent.CAN_FRAME_2):
                yield self._read_can_frame(timestamp, data, pos)
            elif obj_header.obj_type == BlfEvent.CAN_ERROR_EXT:
                yield self._read_error_frame(timestamp, data, pos)
            elif obj_header.obj_type == BlfEvent.CAN_FD_FRAME:
                yield self._read_can_fd_frame(timestamp, data, pos)
            elif obj_header.obj_type == BlfEvent.CAN_FD_FRAME_64:
                yield self._read_can_fd_frame_64(timestamp, data, pos)

            pos = next_pos


if __name__ == "__main__":

    frame1 = LogCanFrame(10.0,1,0x12,0,8,bytearray([0x01,0x02,0x03,0x04,0x05,0x06,0x07]))
    frame2 = LogCanFrame(10.2, 1, 0x12, 0, 8, bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]))
    frame3 = LogCanFrame(10.4, 1, 0x12, 0, 8, bytearray([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]))
    frame4 = copy.deepcopy(frame3)
    frame4.timestamp = 20.3
    frames = [frame1,frame2,frame3,frame4]
    differs = [round(y.timestamp - x.timestamp,7)  for x,y in zip(frames[:-1],frames[1:])]
    for i,frame in enumerate(frames[:-1]):
        frame.period = differs[i]

    for frame in frames:
        print(frame)
    logs = VectorBlfLog(r"C:\Project\SAIC_ZP22\ARiA_Configuration\SpecificCANID.blf")
    for  frame in logs:
        print(frame)

