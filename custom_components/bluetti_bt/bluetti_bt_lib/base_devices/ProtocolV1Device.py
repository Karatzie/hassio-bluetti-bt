"""Base device definition for V1 Protocol devices."""

from typing import List

from ..utils.commands import ReadHoldingRegisters
from ..utils.struct import DeviceStruct
from .BluettiDevice import BluettiDevice


class ProtocolV1Device(BluettiDevice):
    def __init__(self, address: str, type: str, sn: str):
        self.struct = DeviceStruct()

        # Device info
        self.struct.add_string_field("device_type", 10, 6)
        self.struct.add_sn_field("serial_number", 17)

        # Power IO
        self.struct.add_uint_field("dc_input_power", 36)
        self.struct.add_uint_field("ac_input_power", 37)
        self.struct.add_uint_field("ac_output_power", 38)
        self.struct.add_uint_field("dc_output_power", 39)

        # Power IO statistics
        self.struct.add_decimal_field(
            "power_generation", 41, 1
        )  # Total power generated since last reset (kwh)

        # Battery
        self.struct.add_uint_field("total_battery_percent", 43)

        # Battery packs
        self.struct.add_uint_field("pack_num_max", 91)  # internal
        self.struct.add_decimal_field("total_battery_voltage", 92, 1)
        self.struct.add_uint_field("pack_num", 96)  # internal
        self.struct.add_decimal_field("pack_voltage", 98, 2)  # Full pack voltage
        self.struct.add_uint_field("pack_battery_percent", 99)

        # Output state
        self.struct.add_bool_field("ac_output_on", 48)
        self.struct.add_bool_field("dc_output_on", 49)

        # Pack selector
        self.struct.add_uint_field("pack_num", 3006)  # internal

        # Output controls
        self.struct.add_bool_field("ac_output_on_switch", 3007)
        self.struct.add_bool_field("dc_output_on_switch", 3008)

        super().__init__(address, type, sn)

    @property
    def polling_commands(self) -> List[ReadHoldingRegisters]:
        return [
            ReadHoldingRegisters(10, 10),
            ReadHoldingRegisters(36, 4),
            ReadHoldingRegisters(41, 1),
            ReadHoldingRegisters(43, 1),
            ReadHoldingRegisters(91, 2),
            ReadHoldingRegisters(96, 1),
            ReadHoldingRegisters(98, 2),
            ReadHoldingRegisters(48, 2),
        ]

    @property
    def writable_ranges(self) -> List[range]:
        return [range(3006, 3009)]

    @property
    def pack_polling_commands(self) -> List[ReadHoldingRegisters]:
        return [
            ReadHoldingRegisters(91, 2),
            ReadHoldingRegisters(96, 1),
            ReadHoldingRegisters(98, 2),
        ]
