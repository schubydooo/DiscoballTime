import asyncio
import kasa
from kasa import SmartPlug

class KasaStrip():
    '''
    Control a Kasa SmartPlug
    '''
    def __init__(self, discolight_plug, discoball_plug, power_strip_name):

        self.strip = self.connect_to_tp_link_smart_strip(power_strip_name)
        self.discolight_plug = self.get_plug(plug_name=discolight_plug)
        self.discoball_plug = self.get_plug(plug_name=discoball_plug)

        print(f"Discolights Plug -- {self.discolight_plug}")
        print(f"Discoball Plug -- {self.discoball_plug}")

    def get_tp_link_device_ip(self, alias):
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

    def connect_to_tp_link_smart_strip(self, alias):
        '''
        Takes provided alias and returns a SmartStrip object or an error
        '''
        try:
            ip_addr = self.get_tp_link_device_ip(alias)
            # ip_addr = "192.168.0.54"
            strip = kasa.SmartStrip(host=ip_addr)
            asyncio.run(strip.update())
            print(f"Connected to target power strip '{strip.alias}' @ {ip_addr}")

            return strip
        except:
            print("Nobody here")
            return False
    
    def get_plug(self, plug_name):
        '''
        Return list of plug objects that are in the plug names list
        '''
        for plug in self.strip.children:
            if plug.alias in plug_name:
                return plug

        raise TypeError(f"No plug found for {plug_name}")

    def turn_on_plug(self, plug):
        '''
        Turn on the given plugs
        '''
        print (f"Turning on {plug}")
        asyncio.run(plug.turn_on())

    def turn_off_plug(self, plug):
        '''
        Turn off the given plugs
        '''
        print(f"Turning off {plug}")
        asyncio.run(plug.turn_off())

