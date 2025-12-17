import mouse


m = mouse.Mouse(0xfc6d)  # Redragon M811 Aatrox

m.set_poll_rates([1, 1, 1, 1, 1])  # max poll rate (1000Hz)

# keymaps

front_codes = [
    [0x81, 0, 0],  # button 1 = left
    [0x82, 0, 0],  # button 2 = right
    [0x83, 0, 0],  # button 3 = middle
    [0x90, 0, 0x2a],  # button 4 = single key: backspace
    [0x90, 0, 0x28],  # button 5 = single key: return
    [0x8f, 1, 0x1c],  # DPI + = key combo: ctrl + y
    [0x88, 0, 0],  # DPI - = cycle DPIs
    [0x8d, 0, 0],  # mode switch = cycle profiles
]

side_codes0 = [
    [0x8f, 1, 0x7],  # num 1 = ctrl + d
    [0x8f, 1, 0x6],  # num 2 = ctrl + c
    [0x8f, 1, 0x1b],  # num 3 = ctrl + x
    [0x8f, 1, 0x19],  # num 4 = ctrl + v
    [0x8f, 1, 0x13],  # num 5 = ctrl + p
    [0x8f, 2, 0x25],  # num 6 = shift + 8
    [0x90, 0, 0x36],  # num 7 = comma
    [0x90, 0, 0x37],  # num 8 = period
]

# [0x8f, 1, 0x9) = ctrl + f

side_codes1 = [
    [0x90, 0, 0x1e],  # num 1 = 1
    [0x90, 0, 0x1f],  # num 2 = 2
    [0x90, 0, 0x20],  # num 3 = 3
    [0x90, 0, 0x21],  # num 4 = 4
    [0x90, 0, 0x22],  # num 5 = 5
    [0x90, 0, 0x23],  # num 6 = 6
    [0x90, 0, 0x24],  # num 7 = 7
    [0x90, 0, 0x25],  # num 8 = 8
]

m.set_keymap(0, front_codes + side_codes0)
m.set_keymap(1, front_codes + side_codes1)

# DPI

dpi_levels = [
    [0x9, 0],  # 400
    [0x12, 0],  # 800
    [0x1b, 0],  # 1200
    [0x24, 0],  # 1600
    [0x2d, 0],  # 2000
]

m.set_dpis(0, dpi_levels)
m.set_dpis(1, dpi_levels)

# LED effects

effects = [0, 0, 255, 0, 0, 0, 1]  # red, no effects

m.set_effects(0, effects)
m.set_effects(1, effects)
