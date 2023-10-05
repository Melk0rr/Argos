import subprocess, json, re
from typing import List, Dict

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
  def __init__(self, filter: str = "*"):
    """ Constructor """
    self.conditions = []
    self.value = "*"

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

  def get_value(self):
    """ Getter for string value """
    return self.value

  def join_conditions(self):
    """ Recursively joins conditions with separators """
    str_conditions = [ c.to_string() for c in self.conditions ]
    joined = ""
    for i in range(len(str_conditions) - 1):
      joined += f"{str_conditions[i]} {self.conditions_separators[i]} {str_conditions[i+1]}"
      
    return joined

  def to_query_string(self):
    """ Returns a query string """
    query_str = ""
    if len(self.conditions) > 0:
      query_str += "-Filter "

    query_str += f"\"{self.value}\""
    return query_str

def ps_engine(cmd):
  """ Mini engine which provides simple powershell command execution """
  query = subprocess.Popen([
    "pwsh", "-NoLogo", "-NoProfile",
    "-command", cmd
    ],
    text=True,
    encoding='utf-8',
    stdout=subprocess.PIPE
  )
  
  (data, err) = query.communicate()

  if err:
    raise ValueError(f"Argos ps engine::An error occured: {err}")
  return data

def get_ad_user(filter):
  """ Implementation of Get-ADUser command """
  
  ad_filter = ADQueryFilter(filter)
  ad_query = f"get-aduser {ad_filter.to_query_string()}"

  command = f"""
  $test = {ad_query}
  $test | ConvertTo-Json -WarningAction SilentlyContinue
  """

  query = ps_engine(command)
  return json.loads(query)



# test = get_ad_user("Name -like '*lallement*' -and Enabled -eq 'True'")

print(ps_engine("pwd"))
# print(test)