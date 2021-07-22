# pc2s: Portable Conditions and Calibrations Service

The aim of the project is to realize a fully portable, configurable,
experiment-agnostic service for the Conditons and Calibrations data.
Part of it was inspired by the Belle II CDB, however there are significant
differences.

# TZ-aware parsing of time in Django
Example:
```python
temp_date=parse_datetime("2026-07-21 22:50:50+00:00")
```
...which results in
```python
datetime.datetime(2026, 7, 21, 22, 50, 50, tzinfo=datetime.timezone(datetime.timedelta(0), '+0000'))
```

