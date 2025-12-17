# Redragon Mouse Configurator

Python tool to configure Redragon gaming mice via USB

## Usage

The Python module [mouse.py](mouse.py) contains a single class `Mouse`.
It's only dependency is [pyusb](https://github.com/pyusb/pyusb).

To configure a Redragon gaming mouse, create an instance of that class
with the correct Bluetooth product identifier (see [Product IDs](#product-ids)):

```python
from mouse import Mouse

a811 = Mouse(0xfc6d)
```

This object can be used to read and write the mouse configuration (light
effects, poll rate, DPI levels, key mappings) via the proprietary USB control
protocol (reverse engineered by [dokutan/mouse_m908](https://github.com/dokutan/mouse_m908/tree/master)).

For example, to remap the keys:

```python
profile = 0
key_codes = [
    [0x81, 0, 0],  # button 1 = left
    [0x82, 0, 0],  # button 2 = right
    [0x83, 0, 0],  # button3  = middle
    [0x90, 0, 0x2a],  # button 4 = single key: backspace
    [0x90, 0, 0x28],  # button 5 = single key: return
    [0x8f, 1, 0x1c],  # DPI + = key combo: ctrl + y
    [0x88, 0, 0],  # DPI - = cycle DPIs
    [0x8d, 0, 0],  # mode switch = cycle profiles
    [0x90, 0, 0x1e],  # num 1 = 1
    [0x90, 0, 0x1f],  # num 2 = 2
    [0x90, 0, 0x20],  # num 3 = 3
    [0x90, 0, 0x21],  # num 4 = 4
    [0x90, 0, 0x22],  # num 5 = 5
    [0x90, 0, 0x23],  # num 6 = 6
    [0x90, 0, 0x24],  # num 7 = 7
    [0x90, 0, 0x25],  # num 8 = 8
]

a811.set_keymap(profile, key_codes)
```

The number and order of mappable buttons depends on the mouse model.
You can retrieve the current mapping and compare key codes to figure out
which slot represents which button:

```python
a811.print_keymap(profile, 16)  # adjust button count for your device
```

For a list of common key codes, see [Key Codes](#key-codes).

For a list of DPI codes, see [DPI Codes](#dpi-codes).

For a list of poll rate values, see [Poll Rates](#poll-rates).

For a full example, see [example.py](example.py) (my personal configuration script).

## Product IDs

Below is a list of some Redragon USB mouse product IDs.

You can find the product ID of a connected mouse via `lsusb` (on Linux). The 4
digits before the semicolon should be the Holtek Semiconductor vendor ID (04d9),
the 4 digits behind the semicolon are the product ID used to instantiate the
`mouse.Mouse` object.

**PLEASE NOTE THAT THE TOOL WAS NEVER TESTED ON MOST OF THESE MODELS!**

**DOUBLE CHECK THE IDS FOR YOUR DEVIEC AND USE AT YOUR OWN RISK**

| Model | Product ID |
| --- | --- |
| M901 | fc02 |
| M990 | fc0f |
| M709 | fc2a |
| M702 | fc2f |
| M711 | fc30 |
| M602 (RGB) | fc38 |
| M607 | fc38 |
| M715 | fc39 |
| M921 (RGB) | fc40 |
| M990 (RGB) | fc41 |
| M909 | fc42 |
| M802 | fc42 |
| M910 | fc49 |
| M908 | fc4d |
| M719 | fc4f |
| M721 | fc5c |
| M801 (RGB) | fc56 |
| M808 | fc5f |
| M612 | fc61 |
| M811 | fc6d |

## Key Codes

For a complete list see: [dokutan/mouse_m908/blob/master/include/data.cpp](https://github.com/dokutan/mouse_m908/blob/master/include/data.cpp)

### Predefined Key Codes

The `key_code_custom` key code allow sending any key or key combination. For possible
values for `MODIFIER` and `KEY`, see the tables below.

```python
key_code_none = [0x00, 0, 0]

key_code_left = [0x81, 0, 0]
key_code_right = [0x82, 0, 0]
key_code_middle = [0x83, 0, 0]
key_code_backward = [0x84, 0, 0]
key_code_forward = [0x85, 0, 0]
key_code_dpi_cycle = [0x88, 0, 0]
key_code_dpi_down = [0x89, 0, 0]
key_code_dpi_up = [0x8a, 0, 0]
key_code_scroll_up = [0x8b, 0, 0]
key_code_scroll_down = [0x8c, 0, 0]
key_code_profile_switch = [0x8d, 0, 0]

key_code_media_play = [0x8e, 1, 0xcd]
key_code_media_stop = [0x8e, 1, 0xb7]
key_code_media_previous = [0x8e, 1, 0xb6]
key_code_media_next = [0x8e, 1, 0xb5]
key_code_media_volume_up = [0x8e, 1, 0xe9]
key_code_media_volume_down = [0x8e, 1, 0xea]
key_code_media_mute = [0x8e, 1, 0xe2]

key_code_custom = [0x8f, MODIFIER, KEY]

key_code_profile_next = [0x94, 0, 0]
key_code_profile_prev = [0x95, 0, 0]

key_code_report_rate_up = [0x97, 0, 0]
key_code_report_rate_down = [0x98, 0, 0]

key_code_dpi_led_toggle = [0x9b, 1, 0]
key_code_reset_settings = [0x9b, 2, 0]
key_code_led_mode_switch = [0x9b, 4, 0]
```

### Modifier Values

```python
mod_none = 0

# left
mod_ctrl_l = 1
mod_shift_l = 2
mod_alt_l = 4
mod_super_l = 8

# right
mod_ctrl_r = 16
mod_shift_r = 32
mod_alt_r = 64
mod_super_r = 128
```

### Key Values

```python

# alphanumeric
key_a = 0x04
key_b = 0x05
key_c = 0x06
key_d = 0x07
key_e = 0x08
key_f = 0x09
key_g = 0x0a
key_h = 0x0b
key_i = 0x0c
key_j = 0x0d
key_k = 0x0e
key_l = 0x0f
key_m = 0x10
key_n = 0x11
key_o = 0x12
key_p = 0x13
key_q = 0x14
key_r = 0x15
key_s = 0x16
key_t = 0x17
key_u = 0x18
key_v = 0x19
key_w = 0x1a
key_x = 0x1b
key_y = 0x1c
key_z = 0x1d
key_1 = 0x1e
key_2 = 0x1f
key_3 = 0x20
key_4 = 0x21
key_5 = 0x22
key_6 = 0x23
key_7 = 0x24
key_8 = 0x25
key_9 = 0x26
key_0 = 0x27

# modifiers
key_tab = 0x2b
key_caps_Lock = 0x39
key_shift_l = 0xe1
key_ctrl_l = 0xe0
key_alt_l = 0xe2
key_super_l = 0xe3
key_super_r = 0xe7
key_alt_r = 0xe6
key_menu = 0x65
key_ctrl_r = 0xe4
key_shift_r = 0xe5
key_return = 0x28
key_backspace = 0x2a

# special characters
key_space = 0x2c
key_tilde = 0x35
key_minus = 0x2d
key_equals = 0x2e
key_bracket_l = 0x2f
key_bracket_r = 0x30
key_backslash = 0x31
key_hash = 0x32
key_semicolon = 0x33
key_apostrophe = 0x34
key_comma = 0x36
key_period = 0x37
key_slash = 0x38
key_int = 0x64

# navigation
key_right = 0x4f
key_left = 0x50
key_down = 0x51
key_up = 0x52
key_insert = 0x49
key_home = 0x4a
key_pgup = 0x4b
key_delete = 0x4c
key_end = 0x4d
key_pgdown = 0x4e

# top row
key_esc = 0x29
key_f1 = 0x3a
key_f2 = 0x3b
key_f3 = 0x3c
key_f4 = 0x3d
key_f5 = 0x3e
key_f6 = 0x3f
key_f7 = 0x40
key_f8 = 0x41
key_f9 = 0x42
key_f10 = 0x43
key_f11 = 0x44
key_f12 = 0x45
key_prtsc = 0x46
key_scrlk = 0x47
key_pause = 0x48
```

## Poll Rates

```python
poll_1000hz = 1
poll_500hz = 2
poll_250hz = 4
poll_125hz = 8
```

## DPI Codes

```python
dpi_200 = [0x4, 0]
dpi_300 = [0x6, 0]
dpi_400 = [0x9, 0]
dpi_500 = [0xb, 0]
dpi_600 = [0xd, 0]
dpi_700 = [0xf, 0]
dpi_800 = [0x12, 0]
dpi_900 = [0x14, 0]
dpi_1000 = [0x16, 0]
dpi_1100 = [0x18, 0]
dpi_1200 = [0x1b, 0]
dpi_1300 = [0x1d, 0]
dpi_1400 = [0x1f, 0]
dpi_1500 = [0x21, 0]
dpi_1600 = [0x24, 0]
dpi_1700 = [0x26, 0]
dpi_1800 = [0x28, 0]
dpi_1900 = [0x2b, 0]
dpi_2000 = [0x2d, 0]
dpi_2100 = [0x2f, 0]
dpi_2200 = [0x31, 0]
dpi_2300 = [0x34, 0]
dpi_2400 = [0x36, 0]
dpi_2500 = [0x38, 0]
dpi_2600 = [0x3a, 0]
dpi_2700 = [0x3d, 0]
dpi_2800 = [0x3f, 0]
dpi_2900 = [0x41, 0]
dpi_3000 = [0x43, 0]
dpi_3100 = [0x46, 0]
dpi_3200 = [0x48, 0]
dpi_3300 = [0x4a, 0]
dpi_3400 = [0x4d, 0]
dpi_3500 = [0x4f, 0]
dpi_3600 = [0x51, 0]
dpi_3700 = [0x53, 0]
dpi_3800 = [0x56, 0]
dpi_3900 = [0x58, 0]
dpi_4000 = [0x5a, 0]
dpi_4100 = [0x5c, 0]
dpi_4200 = [0x5f, 0]
dpi_4300 = [0x61, 0]
dpi_4400 = [0x63, 0]
dpi_4500 = [0x66, 0]
dpi_4600 = [0x68, 0]
dpi_4700 = [0x6a, 0]
dpi_4800 = [0x6c, 0]
dpi_4900 = [0x6f, 0]
dpi_5000 = [0x71, 0]
dpi_5100 = [0x73, 0]
dpi_5200 = [0x75, 0]
dpi_5300 = [0x78, 0]
dpi_5400 = [0x7a, 0]
dpi_5500 = [0x7c, 0]
dpi_5600 = [0x7f, 0]
dpi_5700 = [0x81, 0]
dpi_5800 = [0x83, 0]
dpi_5900 = [0x85, 0]
dpi_6000 = [0x87, 0]
dpi_6100 = [0x8a, 0]
dpi_6200 = [0x8c, 0]
dpi_6400 = [0x48, 1]
dpi_6600 = [0x4a, 1]
dpi_6800 = [0x4d, 1]
dpi_7000 = [0x4f, 1]
dpi_7200 = [0x51, 1]
dpi_7400 = [0x53, 1]
dpi_7600 = [0x56, 1]
dpi_7800 = [0x58, 1]
dpi_8000 = [0x5a, 1]
dpi_8200 = [0x5c, 1]
dpi_8400 = [0x5f, 1]
dpi_8600 = [0x61, 1]
dpi_8800 = [0x63, 1]
dpi_9000 = [0x66, 1]
dpi_9200 = [0x68, 1]
dpi_9400 = [0x6a, 1]
dpi_9600 = [0x6c, 1]
dpi_9800 = [0x6f, 1]
dpi_10000 = [0x71, 1]
dpi_10200 = [0x73, 1]
dpi_10400 = [0x75, 1]
dpi_10600 = [0x78, 1]
dpi_10800 = [0x7a, 1]
dpi_11000 = [0x7c, 1]
dpi_11200 = [0x7f, 1]
dpi_11400 = [0x81, 1]
dpi_11600 = [0x83, 1]
dpi_11800 = [0x85, 1]
dpi_12000 = [0x87, 1]
dpi_12200 = [0x8a, 1]
dpi_12400 = [0x8c, 1]
```
