##############################################################################
# IPv4 class : provide ipv4 manipulation
##############################################################################
class IPv4 {
  # Attributes
  hidden [byte[]]$bytes = @([byte[]]::new(4))
  hidden [byte[]]$mask  = @([byte[]]::new(4))

  # Constructors
  IPv4([string]$ipString) {
    try {
      $this.bytes = [IPv4]::Parse($ipString)
    }
    catch {
      Write-Error "IPv4::Error while creating new ip address $ipString : $_"
    }
  }

  # Getter for current address bytes
  [byte[]] GetBytes() {
    return $this.bytes
  }

  # Getter for current address mask
  [byte[]] GetMask() {
    return $this.mask
  }

  # Setter for current address mask
  [void] SetMask([string]$maskString) {
    try {
      $this.mask = [IPv4]::Parse($maskString)
    }
    catch {
      Write-Error "IPv4::Invalid mask string provided : $maskString"
    }
  }

  # Converts mask to CIDR notation
  [int] MaskToCIDR() {
    return [IPv4]::BytesToBinaryString($this.mask).Replace(0, "").length
  }

  # Converts current IPv4 address into a string
  [string] ToString([bool]$showMask = $true) {
    $ipString = $this.bytes -join "."

    if ($this.mask -and $showMask) {
      $ipString += "/$($this.MaskToCIDR())"
    }

    return $ipString
  }

  [bool]IsValidSubnet() {
    return $true
  }

  # Parse address string into an array of 4 bytes
  static [byte[]] Parse([string]$ipString) {
    [byte[]]$parse = $ipString.Split(".")

    if ($parse.count -ne 4) {
      throw "IPv4::Invalid address provided : $ipString"
    }

    return $parse
  }

  # Converts array of bytes into a string of bits
  static [string] BytesToBinaryString([byte[]]$bytes) {
    return (-join ($bytes | foreach-object { [convert]::ToString($_, 2) }))
  }

  # Static method to return a subnet mask based on a network length
  static [string] GetSubnetMask([int]$networkLength) {
    if (($networkLength -lt 1) -or ($networkLength -gt 32)) {
      Write-Error "IPv4::Network length must be a value between 1 and 32 !"
      return $null
    }

    $maskBinaryString = ('1' * $networkLength).PadRight(32, '0')
    $maskBinaryArray = $maskBinaryString -split '(.{8})' -ne ''
    [byte[]]$maskBytes = $maskBinaryArray | foreach-object { [convert]::ToInt32($_, 2) }

    return ($maskBytes -join ".")
  }
}


##############################################################################
# Computer class : describing default computer behavior
##############################################################################
class Computer {


}

class ADAccount {

}

class ADComputer: Computer {

}