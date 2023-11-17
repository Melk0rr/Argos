import os, json, re
from typing import List, Dict

from argos.connectors.powershell.engine import ps_engine

folder_path = os.path.dirname(os.path.realpath(__file__))

class ADQueryFilterCondition:
  """ Simple class describing condition for an ad query filter """
  def __init__(self, prop: str, operator: str, value: str):
    """ Constructor """
    self.property = prop
    self.operator = operator
    self.value = value

  def to_string(self) -> str:
    """ Converts current condition into a string """
    return f"{self.property} {self.operator} {self.value}"


class ADQueryFilter:
  """ Simple class to describe Active Directory filter """
  def __init__(self, filter: str = "*", query_type: str):
    """ Constructor """
    self.conditions = []
    self.value = "*"
    self.query_type = query_type

    condition_split = re.split('(-and|-or)', filter)

    if len(condition_split) > 1:
      self.conditions_separators = condition_split[1::2]
    
    for c in condition_split[0::2]:
      raw_condition = c.strip()
      raw_split = raw_condition.split(" ")

      if len(raw_split) == 3:
        prop, operator, value = raw_split
        self.conditions.append(ADQueryFilterCondition(prop, operator, value))

      else:
        self.value = filter

    if len(self.conditions) > 0:
      self.value = self.join_conditions()

  def get_conditions(self) -> List[dict]:
    """ Getter for conditions """
    return self.conditions

  def get_value(self) -> str:
    """ Getter for string value """
    return self.value

  def join_conditions(self) -> str:
    """ Recursively joins conditions with separators """
    str_conditions = [ c.to_string() for c in self.conditions ]
    joined = ""
    for i in range(len(str_conditions) - 1):
      joined += f"{str_conditions[i]} {self.conditions_separators[i]} {str_conditions[i+1]}"
      
    return joined

  def to_query_string(self) -> str:
    """ Returns a query string """
    query_str = ""

    # Handling gpo type : GPO search uses GroupPolicy module not ActiveDirectory module
    if self.query_type == "gpo":
      if self.value == "*":
        query_str += "-All"
      
      else:
        query_str += f"\"{self.value}\""

    # Default behavior using ActiveDirectory module
    else:
      if len(self.conditions) > 0 or self.value == "*":
        query_str += "-Filter "

      query_str += f"\"{self.value}\""

    return query_str


class ADQuery:
  """ Class to provide ad query manipulations through powershell ad """
  ad_commands = {
    "user"    : "Get-ADUser",
    "computer": "Get-ADComputer",
    "group"   : "Get-ADGroup",
    "gpo"     : "Get-GPO"
  }

  def __init__(self, q_type: str = "user", filter: str = "*", properties: List[str] = []):
    """ Constructor """

    if q_type not in self.ad_commands.keys():
      raise ValueError(f"Invalid AD query type provided: {q_type} !")

    self.type = q_type
    self.command = self.ad_commands[q_type]
    self.filter = ADQueryFilter(filter)
    self.properties = properties

    self.credential_paths = {
      "usr": os.path.join(folder_path, "creds", "runner_usr"),
      "pwd": os.path.join(folder_path, "creds", "runner_pwd")
    }

    self.result = []

  def get_credential_usr(self):
    """ Gets the username to use for current query if any """
    if not os.path.isfile(self.credential_paths["usr"]):
      raise OSError(f"Invalid username path: {self.credential_paths['usr']}")

    with open(self.credential_paths["usr"], 'r') as f:
      username = f.readline().strip("\n")

    return username

  def get_credential_pwd(self):
    """ Gets the username to use for current query if any """
    if not os.path.isfile(self.credential_paths["pwd"]):
      raise OSError(f"Invalid password path: {self.credential_paths['pwd']}")

    with open(self.credential_paths["pwd"], 'r') as f:
      pwd = f.readline().strip("\n")

    return pwd

  def set_credential_paths(self, usr: str, pwd: str):
    """ Change credentials path for this query """
    if not os.path.isfile(usr):
      raise OSError(f"Invalid username path: {usr}")

    if not os.path.isfile(pwd):
      raise OSError(f"Invalid username path: {pwd}")

    self.credential_paths["usr"] = usr
    self.credential_paths["pwd"] = pwd

  def clear_results(self):
    """ Clear results """
    self.result.clear()

  def forge(self) -> str:
    """ Forge query to execute """
    base = self.command
    base += f" {self.filter.to_query_string()}"

    if len(self.properties) > 0:
      base += f" -Properties {','.join(self.properties)}"

    return base

  def run(self, server: List[str] = [], use_credentials: bool = False):
    """ Run AD query """

    self.clear_results()
    forged = self.forge()

    if len(server) == 0:
      default_srv = ps_engine("$env:USERDNSDOMAIN")
      server.append(default_srv.strip("\n"))

    for srv in server:
      srv_forged = f"{forged} -Server {srv}"

      srv_command = f"""
      $query = {srv_forged}
      $query | ConvertTo-Json -WarningAction SilentlyContinue
      """

      srv_query = ps_engine(srv_command)
      self.result.append(json.loads(srv_query))

    return self.result

  @staticmethod
  def set_credentials(self, path: str, username: str, password: str):
    """ Set credentials to use for the current query """
    if not os.path.exists(path):
      raise OSError(f"Invalid credentials output path provided: {path}")

    command = f"""
    $username = \"{username}\"
    $username | Out-File \"{path}\"
    $pwd = \"{password}\" | ConvertTo-SecureString -AsPlainText -Force
    $pwd | ConvertFrom-SecureString | Out-File \"{path}\"
    """

    ps_engine(command)


get_user = ADQuery("user", filter="j.lallement")
res = get_user.run()
print(res)
