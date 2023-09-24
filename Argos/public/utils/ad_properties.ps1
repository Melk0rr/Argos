$ADProperties = @{
  ###################################
  # User properties
  ###################################
  user     = @{
    initial = @(
      "Created",
      "Description",
      "EmailAddress",
      "EmployeeID",
      "Title",
      "LastLogonDate",
      "Modified",
      "PasswordLastSet",
      "PasswordNotRequired",
      "PasswordNeverExpires",
      "pwdLastSet"
    )
    final   = @(
      "DistinguishedName",
      "SAN",
      "SID",
      "Name",
      "Surname",
      "GivenName",
      "EmployeeID",
      "Email",
      "DomainName",
      "Status",
      "AccountType",
      "Permissions",
      "CreationDate",
      "LastChangeDate",
      "PasswordNotRequired",
      "PasswordNeverExpires",
      "PasswordLastSet",
      "PasswordLastSetDelta",
      "PasswordShouldBeReset",
      "PasswordChangeAtNextLogon",
      "LastLogonDate",
      "LastLogonDelta",
      "ActivityPeriod",
      "Active (30d)",
      "Active (90d)",
      "Active (180d)",
      "Active (360d)",
      "Health",
      "HealthFlags",
      "Title",
      "Description"
    )
  }

  ###################################
  # Computer properties
  ###################################
  computer = @{
    initial = @(
      "LastLogonDate",
      "Created",
      "Modified",
      "OperatingSystem",
      "OperatingSystemVersion",
      "IPV4Address",
      "PasswordLastSet",
      "PasswordNotRequired",
      "PasswordNeverExpires",
      "Description"
    )
    final   = @(
      "DistinguishedName",
      "SAN",
      "SID",
      "Name",
      "DomainName",
      "Status",
      "ComputerType",
      "OSFamily",
      "OSShort",
      "OSFull",
      "OSEdition",
      "OSVersion",
      "OSBuild",
      "@IPv4",
      "HasExtendedSupport",
      "Support",
      "EndOfSupportDate",
      "SupportStatus",
      "CreationDate",
      "LastChangeDate",
      "PasswordNotRequired",
      "PasswordNeverExpires",
      "PasswordLastSet",
      "PasswordLastSetDelta",
      "PasswordShouldBeReset",
      "LastLogonDate",
      "LastLogonDelta",
      "ActivityPeriod",
      "Active (30d)",
      "Active (90d)",
      "Active (180d)",
      "Active (360d)",
      "Health",
      "HealthFlags",
      "Description"
    )
  }

  ###################################
  # Group properties
  ###################################
  group    = @{
    initial = @(
      "CN",
      "Created",
      "Modified",
      "Description",
      "MemberOf"
    )
    final   = @(
      "DistinguishedName",
      "Name",
      "SID",
      "DomainName",
      "Category",
      "Scope",
      "Members",
      "CreationDate",
      "LastChangeDate",
      "MemberOf",
      "Description"
    )
  }

  ###################################
  # GPO properties
  ###################################
  gpo      = @{
    initial = @(

    )
    final   = @(
      "Name",
      "Id",
      "DomainName",
      "Owner",
      "ImpactedOUs",
      "CreationTime",
      "ModificationTime",
      "Description"
    )
  }

  ###################################
  # OU properties
  ###################################
  ou       = @{
    initial = @(
      "Created",
      "Modified",
      "Description",
      "GPLink"
    )
    final   = @(
      "DistinguishedName",
      "Name",
      "DomainName",
      "Created",
      "Modified",
      "Users",
      "Computers",
      "SubOUs",
      "GPLink",
      "Description"
    )
  }

  ###################################
  # Object properties
  ###################################
  object   = @{
    initial = @(
      "Created",
      "Modified",
      "Description"
    )
    final   = @(
      "DistinguishedName",
      "Name",
      "ObjectClass",
      "DomainName",
      "CreationDate",
      "LastChangeDate",
      "Description"
    )
  }
}