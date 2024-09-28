"""
Custom GATT service implementation
"""
import dbus.service
from common import *
from error_handler import *
from base.gatt_service_base import *
from base.gatt_chrc_base import *


class FleetMgmtService(Service):
    """
    Fleet station service. It will handle the checkup of devices that have exited the bus/tram/etc.
    """
    FLEET_SER_UUID = '77340ad0-c0f8-4a0f-86a2-74c9f0bef9a9'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.FLEET_SER_UUID, True)
        self.add_characteristic(FleetMgmtCharacteristic(bus, 0, self))

class FleetMgmtCharacteristic(Characteristic):

    FLEET_CHRC_UUID = '77341234-c0f8-4a0f-86a2-74c9f0bef9a9'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.FLEET_CHRC_UUID,
                ['notify', 'read', 'write'],
                service)
        self.notifying = False
        self.has_exited = False
        self.has_entered = []
        self.bus_type = None
        self.line = None

        self.value = None


    def _check_enter_flag(self):
        if not self.has_entered[0]:
            return
        else:
            self.has_exited = True
            self.has_entered = False
        
        self.PropertiesChanged(GATT_CHRC_IFACE, { 'has_exited': [True] }, [])

        # ensure that the buffer is clear
        if len(self.has_entered) > 1:
            self._clear_buffer()

        print("Notifying current flag value")

    def _clear_buffer(self, buffer : list) -> None:

        while len(buffer) > 0:
            buffer.pop()

    def ReadValue(self, options):
        """
        Read request for a specific value
        """
        print("Value read : " + str(self.has_entered))
        return self.has_entered
    
    def WriteValue(self, value, options):

        # for now just send 0 or 1 
        if isinstance(value[0], dbus.Byte):
            value = int(value[0])

        if value == 1:
            self.has_entered.append(True)
            print(self.has_entered)

        print("Value written")

    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True
        self._check_enter_flag()

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False