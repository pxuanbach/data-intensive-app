import time
import gc
from typing import Literal, Optional, NoReturn


class TraceTimer:
    """
    timer type can only take the following string values:
    - "performance": the most precise clock in the system.
    - "process": measures the CPU time, meaning sleep time is not measured.
    - "long_running": it is an increasing clock that do not change when the
        date and or time of the machine is changed.
    """

    _counter_start: Optional[int] = None
    _counter_stop: Optional[int] = None

    def __init__(
        self,
        timer_type: Literal["performance", "process", "long_running"] = "performance",
        disable_garbage_collect: bool = True,
    ) -> None:
        self.timer_type = timer_type
        self.disable_garbage_collect = disable_garbage_collect

    def start(self) -> None:
        if self.disable_garbage_collect:
            gc.disable()
        self._counter_start = self._get_counter()

    def stop(self) -> None:
        self._counter_stop = self._get_counter()
        if self.disable_garbage_collect:
            gc.enable()

    @property
    def time_nanosec(self) -> int:
        self._valid_start_stop()
        return self._counter_stop - self._counter_start  # type: ignore

    @property
    def time_sec(self) -> float:
        return self.time_nanosec / 1e9

    def _get_counter(self) -> int:
        counter: int
        if self.timer_type == "performance":
            counter = time.perf_counter_ns()
        elif self.timer_type == "process":
            counter = time.process_time_ns()
        elif self.timer_type == "long_running":
            counter = time.monotonic_ns()
        return counter

    def _valid_start_stop(self) -> Optional[NoReturn]:
        if self._counter_start is None:
            raise ValueError("Timer has not been started.")
        if self._counter_stop is None:
            raise ValueError("Timer has not been stopped.")
        return None
