from time import time, perf_counter_ns
from typing import Optional, Type
from collections import OrderedDict

import contextlib


class Timer:
    """[summary]

    (time_stamp_ns,elapsed)
    """

    def __init__(self, timer_name: str = ""):
        self.timer_name = timer_name
        self.event_record: OrderedDict = OrderedDict()

    def start_timer(self):
        self.event_record = OrderedDict()
        self.start_event("_total_time")

    def end_timer(self):
        total = self.event_record.get("_total_time", None)
        if total is None:
            raise ValueError("Timer has not been started yet.")
        self.event_record["_total_time"]["finish"] = perf_counter_ns()

    def start_event(self, label):
        self.event_record[label] = {"start": perf_counter_ns(), "finish": 0}

    def finish_event(self, label: str):
        if label in self.event_record:
            self.event_record[label]["finish"] = perf_counter_ns()
        else:
            raise ValueError(f"{label} not a valid label.")

    def get_event_time(self, label):
        if label in self.event_record:
            lap = self.event_record[label]["finish"] - self.event_record[label]["start"]
            return lap
        else:
            raise ValueError(f"{label} not a valid label.")

    def format_ns(self, ns, timespec="seconds"):
        if timespec == "seconds":
            return f"{ns/1000000000:9f} seconds."

    def simple_event_message(self, label, timespec="seconds"):
        formatted_nano = self.format_ns(self.get_event_time(label), timespec)
        print(f"{label} took {formatted_nano}")

    def simple_timer_message(self, timespec="seconds"):
        total = self.event_record.get("_total_time", None)
        if total is None:
            raise ValueError("Timer has not been started yet.")
        if total["finish"] == 0:
            raise ValueError("Timer has not been ended yet.")
        formatted_nano = self.format_ns(self.get_event_time("_total_time"))
        print(f"{self.timer_name} took {formatted_nano}")


@contextlib.contextmanager
def simple_timer(label, time_spec="seconds"):
    start = perf_counter_ns()
    yield
    if time_spec == "nanoseconds":
        print(f"{label} took {perf_counter_ns()-start} nano seconds.")
    else:
        print(f"{label} took {(perf_counter_ns()-start)/100000000:9f} seconds.")
