# pyupway

Simple utility to read values from MyUpway cloud service.

## Supported devices

Currently pyupway has been tested on following units

- MCU40
- Jäspi Basic Split 12 kW

## Installation

Install using pip

```
pip install pyupway
```

## Usage

Basic usage is to import MyUpway and MyUpwayConfig from pyupway.

Initialize MyUpwayConfig with proper settings and use it to initialize MyUpway itself. You can obtain heat pump id from the MyUpway UI URL "https://www.myupway.com/System/<heatpumpId>/Status/Overview"

```
from pyupway import MyUpway, MyUpwayConfig, Variable

config = MyUpwayConfig(<username>, <password>, 123456)

myupway = MyUpway(config)

print(myupway.get_current_values([Variable.HIGH_PRESSURE_SENSOR]))
print(myupway.get_history_values(Variable.EXTERNAL_FLOW_TEMP, startDate=datetime(2023,6,1,0,0,0), stopDate=datetime(2023,6,4,0,0,0)))

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

## Variables available

| Enum Name                           | Variable ID | History Data |
| ----------------------------------- | ----------- | ------------ |
| AVG_OUTDOOR_TEMP                    | 40067       | yes          |
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
| ROOM_TEMPERATURE                    | 40033       | yes          |
| ADDITION_BLOCKED                    | 10033       | no           |
| ADDITION_MAX_STEP                   | 47613       | no           |
| ADDITION_STATUS                     | 43091       | yes          |
| ADDITION_FUSE_SIZE                  | 47214       | no           |
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

## Functions

### get_current_values

Returns the current values for selected variables.
Provide variables as a list of Variable enums.

Example

```python
myupway.get_current_values([Variable.HIGH_PRESSURE_SENSOR, Variable.AVG_OUTDOOR_TEMP])
```

### get_history_values

Returns the historical values for specified timerange.

Example

```python
myupway.get_history_values(Variable.EXTERNAL_FLOW_TEMP, startDate=datetime(2023,6,1,0,0,0), stopDate=datetime(2023,6,4,0,0,0))
```
