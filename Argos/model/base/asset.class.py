from enum import Enum
from .ipv4 import IPv4

class AssetType(Enum):
  WS  = "Workstation"
  SRV = "Server"
  UKN = "Unknown"

class Asset:
  """ Asset class describing any kind of IT terminal """

   def __init__(self, name: str, os: str, type: AssetType = AssetType.UKN ip: IPv4 = None):
    """ Constructor """