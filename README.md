# pyupway

Simple utility to read values from either MyUpway or MyUplink cloud service. Currently works only with one system at a time.

When using MyUplink, first visit https://dev.myuplink.com/apps and create new app in order to get the API credentials. Note that History data is not supported with MyUplink service.

## Supported devices

Currently pyupway has been tested on following units

- Jäspi MCU40
- Jäspi Tehowatti AIR
- Jäspi Basic Split 8/12 kW
- Nibe Metro-air 330
- Nibe F470

## Installation

Install using pip

```
pip install pyupway
```

## Usage

Basic usage is to import MyUpway, MyUpwayConfig and DataService from pyupway. Then in Config specify which DataService are you using.

### MyUpway

Initialize MyUpwayConfig with proper settings and use it to initialize MyUpway itself. You can obtain heat pump id from the MyUpway UI URL

```
https://www.myupway.com/System/<heatpumpId>/Status/Overview
```

```python
from pyupway import MyUpway, MyUpwayConfig, Variable, DataService

config = MyUpwayConfig(dataservice=DataService.MYUPWAY, username="<username>", password="<password>", heatpump_id=123456)

myupway = MyUpway(config)

print(myupway.get_current_values([Variable.HIGH_PRESSURE_SENSOR]))
print(myupway.get_history_values(Variable.EXTERNAL_FLOW_TEMP, startDate=datetime(2023,6,1,0,0,0), stopDate=datetime(2023,6,4,0,0,0)))

```

### MyUplink

Get Client ID and Client Secret from MyUplink dev site: https://dev.myuplink.com/apps

Initialize MyUpwayConfig with proper settings and use it to initialize MyUpway itself.

```
https://www.myupway.com/System/<heatpumpId>/Status/Overview
```

```python
from pyupway import MyUpway, MyUpwayConfig, Variable, DataService

config = MyUpwayConfig(dataservice=DataService.MYUPLINK, client_id="<client_id>", client_secret="<client_secret>")

myupway = MyUpway(config)

print(myupway.get_current_values([Variable.HIGH_PRESSURE_SENSOR]))

```

### Data classes

Results are returned in defined dataclasses

#### VariableValue

```python
from pyupway import VariableValue
```

| Field      | Type                                                |
| ---------- | --------------------------------------------------- |
| Id         | int                                                 |
| Name       | str                                                 |
| Enumerator | Variable                                            |
| Value      | int &#124; float &#124; str &#124; bool &#124; None |
| Unit       | str &#124; None                                     |

#### VariableHistoryValue

```python
from pyupway import VariableHistoryValue
```

| Field | Type                                                |
| ----- | --------------------------------------------------- |
| Value | int &#124; float &#124; str &#124; bool &#124; None |
| Unit  | str &#124; None                                     |
| Date  | datetime                                            |

## Data Services

| **Value** | **Meaning**                         |
| --------- | ----------------------------------- |
| MYUPWAY   | Download data from MyUpway service  |
| MYUPLINK  | Download data from MyUplink service |

## Variables available

| Enum Name                           | Variable ID | History Data |
| ----------------------------------- | ----------- | ------------ |
| AVG_OUTDOOR_TEMP                    | 40067       | yes          |
| HOT_WATER_CHARGING                  | 40014       | TBT          |
| HOT_WATER_TOP                       | 40013       | TBT          |
| INDOOR_UNIT_OUTDOOR_TEMP            | 40004       | yes          |
| CURRENT_BE1                         | 40083       | yes          |
| CURRENT_BE2                         | 40081       | yes          |
| CURRENT_BE3                         | 40079       | yes          |
| DEGREE_MINUTES                      | 43005       | yes          |
| EXTERNAL_ADJUSTMENT                 | 43161       | no           |
| FLOOR_DRYING_FUNCTION               | 47276       | no           |
| CALCULATED_FLOW_TEMP                | 43009       | yes          |
| EXTERNAL_FLOW_TEMP                  | 40071       | yes          |
| EXTERNAL_RETURN_TEMP                | 40152       | yes          |
| HEAT_MEDIUM_FLOW                    | 40008       | TBT          |
| HEAT_RETURN_TEMP                    | 40012       | TBT          |
| ROOM_TEMPERATURE                    | 40033       | yes          |
| ADDITION_BLOCKED                    | 10033       | no           |
| ADDITION_MAX_STEP                   | 47613       | no           |
| ADDITION_STATUS                     | 43091       | yes          |
| ADDITION_FUSE_SIZE                  | 47214       | no           |
| ADDITION_TIME_FACTOR                | 43081       | TBT          |
| ADDITION_ELECTRICAL_ADDITION_POWER  | 43084       | TBT          |
| ADDITION_SET_MAX_ELECTRICAL_ADD     | 47212       | TBT          |
| ADDITION_TEMPERATURE                | 40121       | TBT          |
| ENERGY_COOLING_COMPRESSOR_ONLY      | 44302       | TBT          |
| ENERGY_HEATING_COMPRESSOR_ONLY      | 44308       | TBT          |
| ENERGY_HEATING_INT_ADD_INCL         | 44300       | TBT          |
| ENERGY_HOTWATER_COMPRESSOR_ONLY     | 44306       | TBT          |
| ENERGY_HW_INCL_INT_ADD              | 44298       | TBT          |
| ENERGY_POOL_COMPRESSOR_ONLY         | 44304       | TBT          |
| ENERGY_FLOW                         | 40072       | TBT          |
| AUX1                                | 47411       | no           |
| AUX2                                | 47410       | no           |
| AUX3                                | 47409       | no           |
| AUX4                                | 47408       | no           |
| AUX5                                | 47407       | no           |
| AUX6                                | 48366       | no           |
| X7                                  | 47412       | no           |
| COUNTRY                             | 48745       | no           |
| DEFROSTING                          | 44703       | no           |
| CHARGE_PUMP_SPEED                   | 44396       | yes          |
| OUTDOOR_UNIT_OUTDOOR_TEMP           | 44362       | yes          |
| COMPRESSOR_BLOCKED                  | 10014       | no           |
| COMPRESSOR_STARTS                   | 44069       | yes          |
| COMPRESSOR_PROTECTION_MODE          | 44702       | no           |
| CONDENSER_OUT                       | 44058       | yes          |
| EVAPORATOR                          | 44363       | yes          |
| HOT_GAS                             | 44059       | yes          |
| LIQUID_LINE                         | 44060       | yes          |
| RETURN_TEMP                         | 44055       | yes          |
| SUCTION_GAS                         | 44061       | yes          |
| HIGH_PRESSURE_SENSOR                | 44699       | yes          |
| LOW_PRESSURE_SENSOR                 | 44700       | yes          |
| COMPRESSOR_OPERATING_TIME           | 44071       | yes          |
| COMPRESSOR_OPERATING_TIME_HOT_WATER | 44073       | yes          |
| COMPRESSOR_RUN_TIME_COOLING         | 40737       | yes          |
| CURRENT_COMPRESSOR_FREQUENCY        | 44701       | yes          |
| REQUESTED_COMPRESSOR_FREQUENCY      | 40782       | no           |
| VERSION                             | 44014       | no           |
| SMART_PRICE_STATUS                  | 44908       | ??           |
| SMART_PRICE_VALUE                   | 10069       | ??           |
| SMART_PRICE_FACTOR                  | 44896       | ??           |
| COMPRESSOR_EVAPORATOR_TEMP          | 40020       |              |
| COMPRESSOR_TEMP                     | 40023       |              |
| ADDITION_IMMERSION_HEATER_TEMP      | 40024       |              |
| AIR_EXHAUST_TEMP                    | 40025       |              |
| AIR_EXTRACT_TEMP                    | 40026       |              |
| SMART_PRICE_MODE                    | 41929       |              |
| DESIRED_HUMIDITY_1                  | 42770       |              |
| DEFROSTING_TIME                     | 43066       |              |
| FAN_MODE                            | 43108       |              |
| COMPRESSOR_STATUS                   | 43427       |              |
| SMART_PRICE_POOL_OFFSET             | 44898       |              |
| SMART_PRICE_COOLING_OFFSET          | 44899       |              |
| OPERATING_MODE                      | 47137       |              |
| DESIRED_HUMIDITY_2                  | 49633       |              |
| AIR_INCREASED_VENTILATION           | 50005       |              |

## Functions

### get_current_values

Returns the current values for selected variables.
Provide variables as a list of Variable enums.

Example

```python
myupway.get_current_values([Variable.HIGH_PRESSURE_SENSOR, Variable.AVG_OUTDOOR_TEMP])
```

### get_history_values

Returns the historical values for specified timerange. NOT IMPLEMENTED FOR MYUPLINK!

Example

```python
myupway.get_history_values(Variable.EXTERNAL_FLOW_TEMP, startDate=datetime(2023,6,1,0,0,0), stopDate=datetime(2023,6,4,0,0,0))
```
# Contributors
Thank you for contributing to the project!
- lobstaj
- sulate
