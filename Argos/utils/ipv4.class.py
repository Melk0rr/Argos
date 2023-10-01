""" IPv4 module """
from typing import List

from argos.utils.color_print import ColorPrint


class IPv4Base:

  def __init__(self, addr):
    """ Constructor """

    addr_split = addr.split('.')
    if len(addr_split) != 4:
      raise ValueError(f"Invalid IP address provided: {addr}")

    self.address: str = addr
    self.bytes: List[bytes] = [ (int(x)).to_bytes() for x in addr_split ]

  def get_address(self) -> str:
    """ Getter for ip string address """
    return self.address

  def get_bytes(self) -> List[bytes]:
    """ Getter for ip byte array """
    return self.bytes

  def to_hex_array(self) -> List[hex]:
    """ Returns the current ip as hex array """
    return [ x.hex() for x in self.bytes ]

  def to_hex_str(self) -> str:
    """ Returns the current ip as hex string """
    return ''.join(self.to_hex_array())

  def to_binary_array(self) -> List[bin]:
    """ Returns the current ip as a binary table """
    return [ bin(int(x, base=16))[2:] for x in self.to_hex_array() ]

  def to_int(self) -> int:
    """ Returns the current ip as an integer """
    return int(self.to_hex_str(), 16)


class IPv4Mask(IPv4Base):
  """ Simple Class providing tools to manipulate IPv4 mask """

  def __init__(self, mask: int | str):
    """ Constructor """

    if type(mask) is str:
      super().__init__(mask)
      cidr = ''.join(self.to_binary_array()).count('1')
      
    elif type(mask) is int:
      if not 1 < mask < 33:
        raise ValueError("Mask CIDR value must be between 1 and 32!")

      cidr = mask
      super().__init__(self.get_netmask(cidr))
      
    else:
      raise ValueError(f"Invalid mask provided : {mask}. You must provide a string or an integer !")

    self.cidr = cidr

  def get_cidr(self) -> int:
    """ Getter for mask CIDR """
    return self.cidr

  def to_int(self) -> int:
    """ Returns the current mask as an integer """
    return (0xffffffff << (32 - self.cidr)) & 0xffffffff

  @staticmethod
  def get_netcidr(mask: str) -> int:
    """ Static method to return CIDR notation for a given mask """
    if mask not in self.get_valid_mask():
      raise ValueError(f"Invalid mask provided")

    base = IPv4Base(mask)
    return ''.join(base.to_binary_array()).count('1')

  @staticmethod
  def get_valid_mask():
    return [ self.get_netmask(x) for x in range(1, 33) ]

  @staticmethod
  def get_netmask(network_length: int) -> str:
    """ Static method to return an ipv4 mask based on a network length """
    if not type(network_length) is int:
      raise ValueError("Network length must be an integer")
      
    if not 0 < network_length < 33:
      raise ValueError("Network length value must be between 1 and 32!")
    
    mask = (0xffffffff >> (32 - network_length)) << (32 - network_length)
    return (str( (0xff000000 & mask) >> 24) + '.' +
            str( (0x00ff0000 & mask) >> 16) + '.' +
            str( (0x0000ff00 & mask) >> 8)  + '.' +
            str( (0x000000ff & mask)))


class IPv4(IPv4Base):
  """ Simple Class providing tools to manipulate IPv4 addresses """

  def __init__(self, address: str, mask: str = None):
    """ Constructor """
    
    net = mask
    if "/" in address:
      address, net = address.split("/")

    super().__init__(address)

    if net:
      self.mask = IPv4Mask(int(net))

  def get_mask(self) -> IPv4Mask:
    """ Getter for ip mask instance """
    return self.mask

  def set_mask(self, mask: int | str):
    """ Setter for ip mask """
    self.mask = IPv4Mask(mask)

  def is_in_subnet(self, net_addr: str) -> bool:
    """ Checks if the current ip is in the provided subnet """
    if "/" not in net_addr:
      raise ValueError(f"Invalid net address provided ! Please include a net mask as CIDR notation")

    net = IPv4(net_addr)
    mask = net.get_mask().to_int()
    return (self.to_int() & mask) == (net.to_int() & mask)

  def to_string(self, show_mask: bool = True) -> str:
    """ Returns the current instance as a string """
    ip_str = self.address

    if self.mask and show_mask:
      ip_str += f"/{self.mask.get_cidr()}"

    return ip_str


class Subnet:
  """ Simple class to describe Subnet """
  def __init__(self, ip: str, mask: int | str, name: str, location: str, description: str):
    """ Constructor """
    self.ip = IPv4(ip, mask)
    self.name = name
    self.location = location
    self.description = description

    self.hosts: List[IPv4] = []

  def get_ip(self) -> IPv4:
    """ Getter for subnet ip """
    return self.ip

  def get_mask(self) -> IPv4Mask:
    """ Getter for subnet mask """
    return self.ip.get_mask()

  def get_address(self) -> str:
    """ Getter for complete ip address """
    return self.ip.to_string()

  def add_host(self, host: str):
    """ Adds a host address """
    new_host = IPv4(host)
    if new_host.is_in_subnet(self.ip.to_string()):
      self.hosts.append(new_host)
    
    else:
      ColorPrint.red(f"Can't add {host} to {self.ip.to_string()}: invalid ip for this subnet !")



# Tests
ip = IPv4("192.168.1.5/24")
net = Subnet("192.168.1.0", 24)

print(ip.is_in_subnet(net.to_string()))