import ctypes
import ctypes.util


dll = ctypes.util.find_library("libfswatch")
lib = ctypes.CDLL(dll)


fsw_init_library = lib.fsw_init_library


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

fsw_set_recursive = lib.fsw_set_recursive
fsw_set_recursive.restype = ctypes.c_int
fsw_set_recursive.argtypes = [ctypes.c_void_p, ctypes.c_bool]


def _not_implemented():
    raise NotImplementedError()


fsw_add_property = _not_implemented
fsw_set_allow_overflow = _not_implemented
fsw_set_latency = _not_implemented
fsw_set_directory_only = _not_implemented
fsw_set_follow_symlinks = _not_implemented
fsw_add_event_type_filter = _not_implemented
fsw_add_filter = _not_implemented
fsw_last_error = _not_implemented
fsw_is_verbose = _not_implemented
fsw_set_verbose = _not_implemented


def main():

    from threading import Thread
    import signal

    def _callback(events, event_num):
        event = events[0]
        print(event.path.decode())

    assert fsw_init_library() == 0
    handle = fsw_init_session(0)
    assert fsw_add_path(handle, b"/tmp/test/") == 0
    _callback = cevent_callback(_callback)
    assert fsw_set_callback(handle, _callback) == 0
    assert fsw_set_recursive(handle, True) == 0

    # fsw_start_monitor(handle)
    thread = Thread(target=fsw_start_monitor, args=(handle,), daemon=True)

    def handler(signum, frame):
        if fsw_is_running(handle):
            fsw_stop_monitor(handle)
        exit(0)

    signal.signal(signal.SIGINT, handler)

    thread.start()
    thread.join()


if __name__ == "__main__":
    main()
