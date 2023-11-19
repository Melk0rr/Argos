""" Subnet module """
from .ipv4 import IPv4

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