import usb.core
import usb.util

HOLTEK_ID = 0x04d9

INTERFACE = 2

REPORT16 = 0x0302  # Feature Report (0x03), Report ID 0x02 with 16 byte payload
REPORT64 = 0x0303  # Feature Report (0x03), Report ID 0x03 with 64 byte payload

SET_REQUEST_TYPE = usb.util.CTRL_OUT | usb.util.CTRL_TYPE_CLASS | usb.util.CTRL_RECIPIENT_INTERFACE  # 0x21
SET_REPORT = 0x09

GET_REQUEST_TYPE = usb.util.CTRL_IN | usb.util.CTRL_TYPE_CLASS | usb.util.CTRL_RECIPIENT_INTERFACE  # 0xA1
GET_REPORT = 0x01

TIMEOUT = 1000  # 1 second

# memory addresses

SCROLL = (0x20, 0)
ACTIVE = (0x2c, 0)
POLLRATE = (0x32, 0)

DPIS = [(0x42, 0), (0x02, 1), (0xb2, 1), (0x62, 2), (0x12, 3)]

KEYMAPS = [
    [(0x82, 0), (0x86, 0), (0x8a, 0), (0x8e, 0), (0x92, 0), (0x96, 0), (0x9a, 0), (0x9e, 0), (0xa2, 0), (0xa6, 0), (0xaa, 0), (0xae, 0), (0xb2, 0), (0xb6, 0), (0xba, 0), (0xbe, 0), (0xc2, 0), (0xc6, 0), (0xda, 0), (0xde, 0)],
    [(0x42, 1), (0x46, 1), (0x4a, 1), (0x4e, 1), (0x52, 1), (0x56, 1), (0x5a, 1), (0x5e, 1), (0x62, 1), (0x66, 1), (0x6a, 1), (0x6e, 1), (0x72, 1), (0x76, 1), (0x7a, 1), (0x7e, 1), (0x82, 1), (0x86, 1), (0x9a, 1), (0x9e, 1)],
    [(0xf2, 1), (0xf6, 1), (0xfa, 1), (0xfe, 1), (0x02, 2), (0x06, 2), (0x0a, 2), (0x0e, 2), (0x12, 2), (0x16, 2), (0x1a, 2), (0x1e, 2), (0x22, 2), (0x26, 2), (0x2a, 2), (0x2e, 2), (0x32, 2), (0x36, 2), (0x4a, 2), (0x4e, 2)],
    [(0xa2, 2), (0xa6, 2), (0xaa, 2), (0xae, 2), (0xb2, 2), (0xb6, 2), (0xba, 2), (0xbe, 2), (0xc2, 2), (0xc6, 2), (0xca, 2), (0xce, 2), (0xd2, 2), (0xd6, 2), (0xda, 2), (0xde, 2), (0xe2, 2), (0xe6, 2), (0xfa, 2), (0xfe, 2)],
    [(0x52, 3), (0x56, 3), (0x5a, 3), (0x5e, 3), (0x62, 3), (0x66, 3), (0x6a, 3), (0x6e, 3), (0x72, 3), (0x76, 3), (0x7a, 3), (0x7e, 3), (0x82, 3), (0x86, 3), (0x8a, 3), (0x8e, 3), (0x92, 3), (0x96, 3), (0xaa, 3), (0xae, 3)],
]

EFFECTS = [
    (0x49, 4),
    (0x51, 4),
    (0x59, 4),
    (0x61, 4),
    (0x69, 4),
]

# model specific

M811_BUTTONS = [
    "left",
    "right",
    "middle",
    "btn4",
    "btn5",
    "dpiup",
    "dpidown",
    "mode",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num6",
    "num7",
    "num8",
]

M811_ID = 0xfc6d


class Mouse:

    def __init__(self, product_id: int, buttons: list[str]) -> None:

        results = usb.core.find(idVendor=HOLTEK_ID, idProduct=product_id)
        if not isinstance(results, usb.core.Device):
            raise Exception
        self.dev = results

        self.buttons = buttons

        self.was_active = self.dev.is_kernel_driver_active(INTERFACE)
        if self.was_active:
            self.dev.detach_kernel_driver(INTERFACE)

    def close(self) -> None:
        if self.was_active:
            self.dev.attach_kernel_driver(INTERFACE)

    def get_active_profile(self) -> int:
        r = self.read16(ACTIVE, 1)
        return int(r[0])

    def get_poll_rates(self) -> list[int]:
        # 8 = 125Hz, 4=250Hz, 2=500Hz, 1=1000Hz
        r = self.read64(POLLRATE, 10)
        return [r[i] for i in range(0, 10, 2)]

    def get_effects(self, profile: int) -> dict:
        r = self.read16(EFFECTS[profile], 7)
        return {
            "color": r[:3],
            "lightmode": r[3:5],
            "speed": r[5],
            "brightness": r[6],
        }
    
    def get_keymap(self, profile: int) -> dict[str, tuple]:
        # 0x90 0 key 0 = single key
        # 0x8f mod key 0 = combo key (ctrl = 1, shift = 2)
        mapping = {}
        for i, btn in enumerate(self.buttons):
            r = self.read16(KEYMAPS[profile][i], 4)
            mapping[btn] = tuple(r)
        return mapping

    def map_key(self, profile: int, button: str, code: tuple) -> None:
        assert button in self.buttons
        idx = self.buttons.index(button)
        addr = KEYMAPS[profile][idx]
        self.write16(addr, 4, *code)

    def get_dpis(self, profile: int) -> list[tuple]:
        r = self.read64(DPIS[profile], 32)
        # first two bytes skipped, then 5 levels with:
        # (enabled, level low, level high)
        return [tuple(r[i:i+3]) for i in range(2, 32, 6)]

    def set_dpis(self, profile: int, levels: list[tuple]) -> None:
        low, high = DPIS[profile]
        for i, data in enumerate(levels):
            addr = low + 2 + (6 * i), high
            self.write16(addr, 4, *data)

    def get_scroll_speeds(self) -> list[int]:
        r = self.read64(SCROLL, 10)
        return [r[i] for i in range(0, 10, 2)]

    def set_scroll_speeds(self, speeds: tuple) -> None:
        data = [0] * 10
        for i, speed in enumerate(speeds):
            data[i * 2] = speed
        self.write64(SCROLL, 10, *speeds)

    def unlock(self) -> None:
        self._set(REPORT16, [0x02, 0xf5, 0x00] + ([0x00] * 13))

    def lock(self) -> None:
        self._set(REPORT16, [0x02, 0xf5, 0x01] + ([0x00] * 13))

    def read16(self, addr: tuple[int, int], n: int):
        self._set(REPORT16, [0x02, 0xf2, *addr, n] + ([0] * 11))
        return self._get(REPORT16, 16)[8:]

    def read64(self, addr: tuple[int, int], n: int):
        self._set(REPORT64, [0x03, 0xf2, *addr, n] + ([0] * 59))
        return self._get(REPORT64, 64)[8:]

    def write16(self, addr: tuple[int, int], n: int, *args):
        self._set(REPORT16, [0x02, 0xf3, *addr, n, 0, 0, 0, *args] + ([0] * (8 - len(args))))

    def write64(self, addr: tuple[int, int], n: int, *args):
        self._set(REPORT64, [0x03, 0xf3, *addr, n, 0, 0, 0, *args] + ([0] * (56 - len(args))))

    # TODO: 0xf1 function??

    def _set(self, report: int, msg: list[int]):
        sent = self.dev.ctrl_transfer(SET_REQUEST_TYPE, SET_REPORT, report, INTERFACE, bytearray(msg), TIMEOUT)
        assert sent == len(msg)

    def _get(self, report: int, length: int) -> list:
        data = self.dev.ctrl_transfer(GET_REQUEST_TYPE, GET_REPORT, report, INTERFACE, length, TIMEOUT)
        return list(data)
    
