import signal
from threading import Thread

from fswatch import libfswatch


class Monitor:
    def __init__(self):
        assert libfswatch.fsw_init_library() == 0
        self.handle = libfswatch.fsw_init_session(0)
        self._callback = None

        def _callback_wrapper(events, event_num):
            event = events[0]
            self._callback(
                event.path,
                event.evt_time,
                event.flags,
                event.flags_num,
                event_num,
            )

        self._callback_wrapper = _callback_wrapper

    def add_path(self, path: str):
        assert libfswatch.fsw_add_path(self.handle, path.encode()) == 0

    def set_recursive(self, is_recursive=True):
        assert libfswatch.fsw_set_recursive(self.handle, is_recursive) == 0

    def set_callback(self, callback):
        self._callback = callback
        self.cevent_callback = libfswatch.cevent_callback(
            self._callback_wrapper
        )
        assert (
            libfswatch.fsw_set_callback(self.handle, self.cevent_callback) == 0
        )

    def _handle_signal(self, signum, frame):
        if libfswatch.fsw_is_running(self.handle):
            libfswatch.fsw_stop_monitor(self.handle)
        exit(0)

    def start(self):
        """
        This is blocking method which starts monitoring and triggers callback
        """
        signal.signal(signal.SIGINT, self._handle_signal)
        thread = Thread(
            target=libfswatch.fsw_start_monitor,
            args=(self.handle,),
            daemon=True,
        )
        thread.start()
        thread.join()


def main():
    monitor = Monitor()
    monitor.set_recursive()
    monitor.add_path("/tmp/test/")

    def callback(path, evt_time, flags, flags_num, event_num):
        print(path.decode())

    monitor.set_callback(callback)
    monitor.start()


if __name__ == "__main__":
    main()
