import ctypes
import ctypes.util


dll = ctypes.util.find_library('libfswatch')
lib = ctypes.CDLL(dll)

fsw_init_session = lib.fsw_init_session
fsw_init_session.restype = ctypes.c_void_p
fsw_init_session.argtypes = [ctypes.c_int]

fsw_add_path = lib.fsw_add_path
fsw_add_path.restype = ctypes.c_int
fsw_add_path.argtypes = [ctypes.c_void_p, ctypes.c_char_p]


class fsw_cevent(ctypes.Structure):
    _fields_ = [
        ("path", ctypes.c_char_p),
        ("evt_time", ctypes.c_int),
        ("flags", ctypes.c_void_p),
        ("flags_num", ctypes.c_uint),
    ]


cevent_callback = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(fsw_cevent), ctypes.c_uint
)

fsw_set_callback = lib.fsw_set_callback
fsw_set_callback.restype = ctypes.c_int
fsw_set_callback.argtypes = [ctypes.c_void_p, cevent_callback]

fsw_start_monitor = lib.fsw_start_monitor
fsw_start_monitor.restype = ctypes.c_int
fsw_start_monitor.argtypes = [ctypes.c_void_p]

fsw_is_running = lib.fsw_is_running
fsw_is_running.restype = ctypes.c_bool
fsw_is_running.argtypes = [ctypes.c_void_p]

fsw_stop_monitor = lib.fsw_start_monitor
fsw_stop_monitor.restype = ctypes.c_int
fsw_stop_monitor.argtypes = [ctypes.c_void_p]

fsw_destroy_session = lib.fsw_destroy_session
fsw_destroy_session.restype = ctypes.c_int
fsw_destroy_session.argtypes = [ctypes.c_void_p]


def _not_implemented():
    raise NotImplementedError()


fsw_add_property = _not_implemented
fsw_set_allow_overflow = _not_implemented
fsw_set_latency = _not_implemented
fsw_set_recursive = _not_implemented
fsw_set_directory_only = _not_implemented
fsw_set_follow_symlinks = _not_implemented
fsw_add_event_type_filter = _not_implemented
fsw_add_filter = _not_implemented
fsw_last_error = _not_implemented
fsw_is_verbose = _not_implemented
fsw_set_verbose = _not_implemented


def callback(events, event_num):
    event = events[0]
    print(event.path.decode())


def main():

    from threading import Thread
    import signal

    assert lib.fsw_init_library() == 0
    handle = fsw_init_session(0)

    def handler(signum, frame):
        if fsw_is_running(handle):
            print('Stopping', fsw_stop_monitor(handle))

    signal.signal(signal.SIGINT, handler)

    assert fsw_add_path(handle, ctypes.c_char_p(b'/tmp/test/')) == 0

    _callback = cevent_callback(callback)
    assert fsw_set_callback(handle, _callback) == 0

    thread = Thread(target=fsw_start_monitor, args=(handle,))
    thread.start()
    print('Started')
    print('Stopping')
    print(fsw_stop_monitor(handle))
    print('Waiting...')
    thread.join()


if __name__ == '__main__':
    main()
