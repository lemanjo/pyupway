# v0.0.15

- ADD: Fetch MyUpway boolean values in English
- ADD: Retrieve and provide device id
- FIX: Login failed with MyUpwayService
- PROJECT: Implement GitHub Actions for pypi publish

# v0.0.14

- FIX: Duplicated variable PUMP_HEATING_MEDIUM
- FIX: isOnline state not updating
- FIX: MyUpway Service calling old login method
- ADD: New variables for Nibe

# v0.0.13

- FIX: Unknown enum handling

# v0.0.12

- FIX: Import order

# v0.0.11

- FIX: More old python version fixes

# v0.0.10

- FIX: Support for Python version 3.8 & 3.9

# v0.0.9

- FIX: Missing Logout implementation

## Other Stuff

- Read previous releasen notes for 0.0.8

# v0.0.8

- ADD: Integration for MyUplink service

## Other Stuff

- This release includes breaking changes! Basically all the previous MyUpway functionality is there, but you need to update the configurations. Make sure you define the DataService you want to use and be specific of what you specify.

# v0.0.7

- ADD: Smart Price enums
- FIX: Regex breaking with negative values
- FIX: Regex breaking with comma decimal separator

## Other Stuff

- Code was tested working with Nibe Metro-Air 330
