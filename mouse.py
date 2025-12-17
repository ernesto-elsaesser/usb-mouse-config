import usb.core
import usb.util


VENDOR_ID = 0x04d9  # Holtek

INTERFACE = 2

# HID custom feature report constants

SET_REQUEST_TYPE = usb.util.CTRL_OUT | usb.util.CTRL_TYPE_CLASS | usb.util.CTRL_RECIPIENT_INTERFACE  # 0x21
SET_REPORT = 0x09

GET_REQUEST_TYPE = usb.util.CTRL_IN | usb.util.CTRL_TYPE_CLASS | usb.util.CTRL_RECIPIENT_INTERFACE  # 0xA1
GET_REPORT = 0x01

FEATURE_REPORT = 0x0300
LEN_16B = 0x02  # 16 byte payloads
LEN_64B = 0x03  # 64 byte payloads
REPORT_16B = FEATURE_REPORT | LEN_16B
REPORT_64B = FEATURE_REPORT | LEN_64B

OP_SEEK = 0xf2
OP_WRITE = 0xf3
OP_LOCK = 0xf5

TIMEOUT = 1000  # 1 second

# mouse memory addresses

ADR_SCROLL = (0x20, 0)
ADR_ACTIVE = (0x2c, 0)
ADR_POLLRATE = (0x32, 0)

ADR_DPIS = [(0x42, 0), (0x02, 1), (0xb2, 1), (0x62, 2), (0x12, 3)]

ADR_KEYMAPS = [
    [(0x82, 0), (0x86, 0), (0x8a, 0), (0x8e, 0), (0x92, 0), (0x96, 0), (0x9a, 0), (0x9e, 0), (0xa2, 0), (0xa6, 0), (0xaa, 0), (0xae, 0), (0xb2, 0), (0xb6, 0), (0xba, 0), (0xbe, 0), (0xc2, 0), (0xc6, 0), (0xda, 0), (0xde, 0)],
    [(0x42, 1), (0x46, 1), (0x4a, 1), (0x4e, 1), (0x52, 1), (0x56, 1), (0x5a, 1), (0x5e, 1), (0x62, 1), (0x66, 1), (0x6a, 1), (0x6e, 1), (0x72, 1), (0x76, 1), (0x7a, 1), (0x7e, 1), (0x82, 1), (0x86, 1), (0x9a, 1), (0x9e, 1)],
    [(0xf2, 1), (0xf6, 1), (0xfa, 1), (0xfe, 1), (0x02, 2), (0x06, 2), (0x0a, 2), (0x0e, 2), (0x12, 2), (0x16, 2), (0x1a, 2), (0x1e, 2), (0x22, 2), (0x26, 2), (0x2a, 2), (0x2e, 2), (0x32, 2), (0x36, 2), (0x4a, 2), (0x4e, 2)],
    [(0xa2, 2), (0xa6, 2), (0xaa, 2), (0xae, 2), (0xb2, 2), (0xb6, 2), (0xba, 2), (0xbe, 2), (0xc2, 2), (0xc6, 2), (0xca, 2), (0xce, 2), (0xd2, 2), (0xd6, 2), (0xda, 2), (0xde, 2), (0xe2, 2), (0xe6, 2), (0xfa, 2), (0xfe, 2)],
    [(0x52, 3), (0x56, 3), (0x5a, 3), (0x5e, 3), (0x62, 3), (0x66, 3), (0x6a, 3), (0x6e, 3), (0x72, 3), (0x76, 3), (0x7a, 3), (0x7e, 3), (0x82, 3), (0x86, 3), (0x8a, 3), (0x8e, 3), (0x92, 3), (0x96, 3), (0xaa, 3), (0xae, 3)],
]

ADR_EFFECTS = [
    (0x49, 4),
    (0x51, 4),
    (0x59, 4),
    (0x61, 4),
    (0x69, 4),
]


class Mouse:

    def __init__(self, product_id: int) -> None:
        results = usb.core.find(idVendor=VENDOR_ID, idProduct=product_id)
        if not isinstance(results, usb.core.Device):
            raise AttributeError(f"No USB device with ID {VENDOR_ID:04x}:{product_id:04x}")
        self.dev: usb.core.Device = results

    def get_active_profile(self) -> int:
        self._unlock()
        data = self._read16(ADR_ACTIVE, 1)
        self._lock()
        return data[0]

    def get_poll_rates(self) -> list[int]:
        # 8 = 125Hz, 4=250Hz, 2=500Hz, 1=1000Hz
        self._unlock()
        data = self._read64(ADR_POLLRATE, 10)
        self._lock()
        return [data[i] for i in range(0, 10, 2)]

    def set_poll_rates(self, rates: list[int]) -> None:
        gapped = [v for r in rates for v in (r, 0)]
        self._unlock()
        self._write64(ADR_POLLRATE, 10, *gapped)
        self._lock()

    def get_effects(self, profile: int) -> list[int]:
        self._unlock()
        effects = self._read16(ADR_EFFECTS[profile], 7)
        self._lock()
        # R, G, B, lightmode_low, speed, lightmode_high, brightness
        return effects

    def set_effects(self, profile: int, effects: list[int]) -> None:
        self._unlock()
        self._write16(ADR_EFFECTS[profile], 7, *effects)
        self._lock()
    
    def get_keymap(self, profile: int, size: int) -> list[list[int]]:
        addrs = ADR_KEYMAPS[profile]
        self._unlock()
        codes = [self._read16(addrs[i], 4) for i in range(size)]
        self._lock()
        return codes
    
    def print_keymap(self, profile: int, size: int) -> None:
        codes = self.get_keymap(profile, size)
        for i, code in enumerate(codes):
            print(f"{i:02} - 0x{code[0]:02x} 0x{code[1]:02x} 0x{code[2]:02x}")

    def set_keymap(self, profile: int, codes: list[list[int]]) -> None:
        addrs = ADR_KEYMAPS[profile]
        self._unlock()
        for addr, code in zip(addrs, codes):
            self._write16(addr, 4, *code)
        self._lock()

    def get_dpis(self, profile: int) -> list[list]:
        self._unlock()
        dpi_codes = self._read64(ADR_DPIS[profile], 32)
        self._lock()
        # first two bytes skipped, unused
        levels = [dpi_codes[i+1:i+3] for i in range(2, 32, 6)
                  if dpi_codes[i] == 1]
        return levels

    def set_dpis(self, profile: int, levels: list[list]) -> None:
        dpi_codes = [[1, l, h] for l, h in levels]
        while len(dpi_codes) < 5:
            dpi_codes.append([0, 0, 0])
        addr = ADR_DPIS[profile]
        self._unlock()
        for i, data in enumerate(dpi_codes):
            level_addr = addr[0] + 2 + (6 * i), addr[1]
            self._write16(level_addr, 4, *data)
        self._lock()

    def get_scroll_speeds(self) -> list[int]:
        self._unlock()
        data = self._read64(ADR_SCROLL, 10)
        self._lock()
        return [data[i] for i in range(0, 10, 2)]

    def set_scroll_speeds(self, speeds: list[int]) -> None:
        gapped = [v for s in speeds for v in (s, 0)]
        self._unlock()
        self._write64(ADR_SCROLL, 10, *gapped)
        self._lock()

    def _read16(self, addr: tuple[int, int], n: int) -> list[int]:
        self._set(REPORT_16B, [LEN_16B, OP_SEEK, *addr, n], 16)
        return self._get(REPORT_16B, 16)

    def _read64(self, addr: tuple[int, int], n: int) -> list[int]:
        self._set(REPORT_64B, [LEN_64B, OP_SEEK, *addr, n], 64)
        return self._get(REPORT_64B, 64)

    def _write16(self, addr: tuple[int, int], n: int, *args):
        self._set(REPORT_16B, [LEN_16B, OP_WRITE, *addr, n, 0, 0, 0, *args], 16)

    def _write64(self, addr: tuple[int, int], n: int, *args):
        self._set(REPORT_64B, [LEN_64B, OP_WRITE, *addr, n, 0, 0, 0, *args], 64)

    def _unlock(self) -> None:
        self._set(REPORT_16B, [LEN_16B, OP_LOCK, 0], 16)

    def _lock(self) -> None:
        self._set(REPORT_16B, [LEN_16B, OP_LOCK, 1], 16)

    def _set(self, report: int, msg: list[int], length: int):
        pad = [0] * (length - len(msg))
        data = bytearray(msg + pad)
        sent = self.dev.ctrl_transfer(SET_REQUEST_TYPE, SET_REPORT, report, INTERFACE, data, TIMEOUT)
        assert sent == length

    def _get(self, report: int, length: int) -> list[int]:
        data = self.dev.ctrl_transfer(GET_REQUEST_TYPE, GET_REPORT, report, INTERFACE, length, TIMEOUT)
        return list(data[8:])
