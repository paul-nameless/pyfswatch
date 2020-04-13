# Python fswatch

Cross-platform filesystem event monitor for Python.

This is wrapper for the [libfswatch](https://github.com/emcrisostomo/fswatch/)


## Install

```sh
brew install fswatch
pip install fswatch
```


## Usage

```python
from fswatch import Monitor

monitor = Monitor()
monitor.add_path("/tmp/test/")


def callback(path, evt_time, flags, flags_num, event_num):
    print(path.decode())


monitor.set_callback(callback)
monitor.start()
```

Low level functions can be accessed via `libfswatch` module.

It is implemented one to one with this [header file](https://github.com/emcrisostomo/fswatch/blob/master/libfswatch/src/libfswatch/c/libfswatch.h)

```python
from fswatch import libfswatch

libfswatch.fsw_init_library()
handle = fsw_init_session(0)
...
```
