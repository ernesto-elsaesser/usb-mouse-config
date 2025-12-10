#%%
import mouse

#%%
# NOTE: requires root!
m811 = mouse.Mouse(mouse.M811_ID, mouse.M811_BUTTONS)

#%%
m811.unlock()

#%%
PROFILE = 0
keymap = m811.get_keymap(PROFILE)
for btn, code in keymap.items():
    print(btn, hex(code[0]), hex(code[1]), hex(code[2]))

#%%
m811.map_key(PROFILE, "num1", (0x8f, 1, 0x9)) # ctrl + f

#%%
m811.lock()