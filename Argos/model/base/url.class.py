""" URL module adressing url object behaviour """
import re
import socket
from urllib.parse import urlparse, urlsplit

from .port import Port
from argos.utils.color_print import ColorPrint


class URL:
  """ URL class implementation """

  def __init__(self, url):
    """ Constructor """
    # Inject protocol if not there
    if not re.match(r'http(s?):', url):
      url = 'http://' + url

    if not self.is_valid_url(url):
      raise ValueError(f"Invalid URL provided: {url} !")

    self.host = url
    self.netloc = self.extract_domain()
    self.ip = ""
    self.ports = []
    self.related_domains = []

  def get_host(self):
    """ Getter for the URL """
    return self.host

  def get_ip(self):
    """ Getter for the IP """
    return self.ip

  def get_netloc(self):
    """ Getter for the Domain """
    return self.netloc

  def get_port_numbers(self):
    """ Getter for the Port numbers """
    return [p.get_number() for p in self.open_ports]

  def get_port_strings(self):
    """ Getter for the Port strings """
    return [p.to_string() for p in self.open_ports]

  def set_open_ports(self, ports):
    """ Set the open ports """
    # Clear the list of open ports
    self.open_ports.clear()

    for p in ports:
      self.append_open_port(p)

  def set_related_domains(self, domains):
    """ Set the host related domains """
    self.related_domains = domains

  def is_port_in_list(self, port):
    """ Check if the given port is in the list of ports """
    port_number = port

    if isinstance(port, Port):
      port_number = port.get_number()

    return port_number in self.get_port_numbers()

  def append_open_port(self, port):
    """ Append the port to the list of open ports """
    is_port = isinstance(port, Port)
    is_number = isinstance(port, int)

    if not (is_port or is_number):
      raise ValueError(
          "Provided port must be an instance of class Port or an integer")

    if not self.is_port_in_list(port):
      if is_number:
        port = Port(port_number=port)

      self.open_ports.append(port)

    else:
      print(f"This port is already in the list of open ports")

  def remove_port(self, port):
    """ Remove the port from the list of open ports """
    index = self.get_port_numbers().index(port)

    del self.open_ports[index]

  def extract_domain(self):
    """ Extract domain from url """
    return urlsplit(self.host).netloc

  def is_valid_url(self, url):
    """ Checks whether the given URL is valid """
    try:
      parsed = urlparse(url)
      return all([parsed.scheme, parsed.netloc])

    except:
      return False

  def resolve_ip(self):
    """ Resolves the IP address for the current URL """
    try:
      ip = socket.gethostbyname(self.netloc)
      self.ip = ip
      ColorPrint.green(f"{self.netloc}: {self.ip}")

    except:
      ColorPrint.red(f"Could not resolve IP address for {self.netloc}")

  def to_dictionary(self):
    """ Returns a dictionary based on the instance attributes """
    return {
        "host": self.netloc,
        "ip": self.ip,
        **self.geo_location,
        "domains": ', '.join(f"{x}" for x in self.related_domains),
        "ports": ', '.join(f"{x}" for x in self.get_port_numbers()),
        "products": ', '.join(f"{x}" for x in self.get_port_strings())
    }
