# Change Log of Cerium Library

## [1.2.5] - 2019-01-26
### Added
- Add long press function for simulating finger long press somewhere.

```python
from cerium import AndroidDriver

driver = AndroidDriver(wireless=True, host='192.168.124.12')
driver.long_press(570, 1560, 1000)
```
