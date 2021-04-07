import asyncio
import kasa 
from kasa import SmartPlug

# TODO: Move this into a config file
DISCO_POWER_STRIP = "TP-LINK_Smart Plug_8817"
PLUG_NAMES_PRE_DROP = ['Disco Light']
PLUG_NAMES_POST_DROP = ['Discoball']

# plug = kasa.SmartPlug(host="192.168.0.54")
# asyncio.run(plug.update())
# print(plug.alias)
# asyncio.run(plug.turn_off())

def get_tp_link_device_ip(alias):
    '''
    Scan the network to find a specified TP-Link device alias
    '''
    devices = asyncio.run(kasa.Discover.discover())
    target_addr = False
    for addr, dev in devices.items():
        asyncio.run(dev.update())
        if dev.alias == alias:
            target_addr = addr 
    
    return target_addr

def turn_on_plugs(plug_list):
    '''
    Turn on the given plug
    '''
    for plug in plug_list:
        asyncio.run(plug.turn_on())

def turn_off_plugs(plug_list):
    '''
    Turn off the given plug
    '''
    for plug in plug_list:
        asyncio.run(plug.turn_off())

def connect_to_tp_link_smart_strip(alias):
    '''
    Takes provided alias and returns a SmartStrip object or an error
    '''
    try:
        # ip_addr = get_tp_link_device_ip(DISCO_POWER_STRIP)
        ip_addr = "192.168.0.54"
        strip = kasa.SmartStrip(host=ip_addr)
        asyncio.run(strip.update())
        print(f"Connected to target power strip '{strip.alias}' @ {ip_addr}")

        return strip
    except: 
        print("Nobody here")
        return False


def get_plugs_in_group(strip, plug_names):
    '''
    Return list of plug objects that are in the plug names list
    '''
    plug_list = []
    for plug in strip.children:
        if plug.alias in plug_names:
            plug_list.append(plug)

    return plug_list

            

strip = connect_to_tp_link_smart_strip(DISCO_POWER_STRIP)
plugs_pre_drop = get_plugs_in_group(strip=strip, plug_names=PLUG_NAMES_PRE_DROP)
plugs_post_drop = get_plugs_in_group(strip=strip, plug_names=PLUG_NAMES_POST_DROP)

print(f"PRE -- {plugs_pre_drop}")
print(f"POST -- {plugs_post_drop}")

turn_off_plugs(plugs_pre_drop)