from PySide2 import QtNetwork
from PySide2 import QtCore
from .device import Device
from struct import Struct

class Broadcaster():
    def __init__(self):
        self._other_devices = set()
        self._socket =  QtNetwork.QUdpSocket()
        self._broadcast_port = 45454
        self._socket.bind(self._broadcast_port)
        self._socket.readyRead.connect(self.process_broadcast)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.send_broadcast)
        self.this_device = Device()
        self.this_device.set_this_device()

    def get_broadcast_port(self):
        return self._broadcast_port

    def get_other_devices(self):
        return self._other_devices

    def get_broadcast_addresses(self):
        broadcast_addresses = set()        
        interfaces = QtNetwork.QNetworkInterface.allInterfaces()        
        for interface in interfaces:
            if (interface.CanBroadcast):
                address_entries = interface.addressEntries()
                for i in range(len(address_entries)):
                    if address_entries[i].broadcast().isLoopback() or address_entries[i].broadcast().isNull():
                        pass
                    else:
                        broadcast_addresses.add(address_entries[i].broadcast().toString())
        return broadcast_addresses

    def send_broadcast(self):
        broadcast_addresses = self.get_broadcast_addresses()        
        for address in broadcast_addresses:
            datagram = self.this_device.get_name()
            self._socket.writeDatagram(QtCore.QByteArray(bytes(datagram, "ascii")), QtNetwork.QHostAddress(address), self._broadcast_port)

    def process_broadcast(self):
        while self._socket.hasPendingDatagrams():
            name, host, port = self._socket.readDatagram(self._socket.pendingDatagramSize())            
            if self.this_device.get_ip_address().isEqual(host, QtNetwork.QHostAddress.ConvertV4MappedToIPv4):
                return
            host.setAddress(host.toIPv4Address())
            found = False
            for device in self._other_devices:
                if device.get_ip_address() == host:
                    found = True
                    return
            if not found:
                new_device = Device()
                new_device.set_name(str(name.data(), encoding="ascii"))
                new_device.set_ip_address(host)
                self._other_devices.add(new_device)

    def start_broadcast(self):
        self.send_broadcast()
        if not self._timer.isActive():
            self._timer.start(5000)