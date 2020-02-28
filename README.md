# Python fswatch

Python wrapper for the [libfswatch](https://github.com/emcrisostomo/fswatch/)


## Install

```sh
brew install fswatch
pip install fswatch
```


## Usage

```python
monitor = Monitor()
monitor.add_path('/tmp/test/')

def callback(path, evt_time, flags, flags_num, event_num):
    print(path.decode())
monitor.set_callback(callback)
monitor.start()
```
