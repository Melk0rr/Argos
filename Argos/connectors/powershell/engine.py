import subprocess

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