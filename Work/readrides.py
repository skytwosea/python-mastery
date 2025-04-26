import csv
from collections import namedtuple
from dataclasses import dataclass
import polars as pl
import tracemalloc
import time



def length_formatter(length: int) -> float:
  """Format an integer-as-string as a human-readable file size string."""
  try:
      n = float(length)
  except Exception:
      return "-"
  for unit in ["b", "Kb", "Mb", "Gb", "Tb"]:
      if abs(n) < 1024.0:
          return f"{n:3.1f} {unit}"
      n /= 1024.0
  return f"{n:.1f} Pb"

nt_row = namedtuple('NtRow', ['route', 'date', 'daytype', 'rides'])

class ClassRow:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = int(rides)

@dataclass
class DataclassRow:
    route: str
    date: str
    daytype: str
    rides: int

class SlottedClassRow:
    __slots__ = ("route", "date", "daytype", "rides")
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = int(rides)

@dataclass
class SlottedDataclassRow:
    __slots__ = ("route", "date", "daytype", "rides")
    route: str
    date: str
    daytype: str
    rides: int

def create_object(identifier, route, date, daytype, rides):
    match(identifier):
        case "tuple":
            return (route, date, daytype, int(rides))
        case "namedtuple":
            return nt_row(route, date, daytype, int(rides))
        case "dict":
            return {
                "route": route,
                "date": date,
                "daytype": daytype,
                "rides": int(rides),
            }
        case "class":
            return ClassRow(route, date, daytype, rides)
        case "dataclass":
            return DataclassRow(route, date, daytype, rides)
        case "slotted_class":
            return SlottedClassRow(route, date, daytype, rides)
        case "slotted_dataclass":
            return SlottedDataclassRow(route, date, daytype, rides)
        case _:
            pass





def read_rides_memory(filename, fn_key) -> tuple:
    tracemalloc.start()
    t0 = time.monotonic()
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = create_object(fn_key, route, date, daytype, rides)
            records.append(record)
    t1 = time.monotonic()
    cur, pk = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tracemalloc.clear_traces()
    runtime = t1 - t0
    return (cur, pk, runtime)

def read_into_pldf(filename) -> tuple:
    tracemalloc.start()
    t0 = time.monotonic()
    df = pl.read_csv(filename)
    _ = df.select(pl.sum("rides"))
    t1 = time.monotonic()
    cur, pk = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tracemalloc.clear_traces()
    rt = t1 - t0
    return (cur, pk, rt)

if __name__ == '__main__':
    fn_lst = [
        "tuple",
        "namedtuple",
        "dict",
        "class",
        "dataclass",
        "slotted_class",
        "slotted_dataclass",
    ]
    for key in fn_lst:
        cur, pk, rt = read_rides('Data/ctabus.csv', key)
        print(f"{key.upper()}:\n  mem_current: {length_formatter(cur)}\n     mem_peak: {length_formatter(pk)}\n      runtime: {rt}")
    cur, pk, rt = read_into_pldf('Data/ctabus.csv')
    print(f"POLARS:\n  mem_current: {length_formatter(cur)}\n     mem_peak: {length_formatter(pk)}\n      runtime: {rt}")
