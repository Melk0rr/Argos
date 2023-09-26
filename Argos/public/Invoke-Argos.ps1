function Invoke-Argos {
  <#
  .SYNOPSIS
    This script will retreive various informations and generate csv files in order to produce security KPIs

  .NOTES
    Name: Invoke-KPIRetreiver
    Author: JL
    LastUpdated: 2023-09-26

  .EXAMPLE
    Invoke-Argos
  #>

  [CmdletBinding()]
  param(

    [Parameter(
      Mandatory = $false,
      ValueFromPipeline = $false,
      ValueFromPipelineByPropertyName = $false
    )]
    [ValidateNotNullOrEmpty()]
    [switch]  $Help,

    [Parameter(
      Mandatory = $false,
      ValueFromPipeline = $false,
      ValueFromPipelineByPropertyName = $false
    )]
    [ValidateNotNullOrEmpty()]
    [switch]  $Version
  )

  BEGIN {

    # If using help or version options, just write and exit
    if ($Help.IsPresent) {
      Write-Host $docString
      continue
    }

    if ($Version.IsPresent) {
      Write-Host (Get-ModuleVersion)
      continue
    }

    Write-Host $banner -f Cyan

    $startTime = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $day = ($startTime -split " ")[0].Replace('-', '')


    $csvExportParams = @{ Delimiter = '|'; Encoding = "utf8" }
  }

  PROCESS {

  }

  END {
    $endTime = Get-Date
    
  }
}