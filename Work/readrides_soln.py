import csv
import collections

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

class RideData(collections.abc.Sequence):
    def __init__(self):
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        assert all(
            len(attr) == len(self.routes)
            for attr in [self.dates, self.daytypes, self.numrides]
        )
        return len(self.routes)

    def __getitem__(self, index: int|slice):
        if isinstance(index, int):
            return {
                'route': self.routes[index],
                'date': self.dates[index],
                'daytype': self.daytypes[index],
                'rides': self.numrides[index],
            }
        elif isinstance(index, slice):
            rtn_val = []
            _start = index.start if index.start else 0
            _stop = index.stop if index.stop else 0
            _step = index.step if index.step else 1
            for i in range(_start, _stop, _step):
                rtn_val.append(
                    {
                        'route': self.routes[i],
                        'date': self.dates[i],
                        'daytype': self.daytypes[i],
                        'rides': self.numrides[i],
                    }
                )
            return rtn_val
        else:
            return NotImplemented

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])

def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records

def read_rides_as_dicts(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                'route': route, 
                'date': date, 
                'daytype': daytype, 
                'rides' : rides
                }
            records.append(record)
    return records

class Row:
    # Uncomment to see effect of slots
    __slots__ = ('route', 'date', 'daytype', 'rides')
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

# Uncomment to use a namedtuple instead
# from collections import namedtuple
# Row = namedtuple('Row',('route','date','daytype','rides'))

def read_rides_as_instances(filename):
    '''
    Read the bus ride data as a list of instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records

def read_rides_as_columns(filename):
    '''
    Read the bus ride data into 4 lists, representing columns
    '''
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename, "r") as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(row[3])
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)



if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    read_rides = read_rides_as_instances # Change to as_dicts, as_instances, etc.
    rides = read_rides("Data/ctabus.csv")
    cur, pk = tracemalloc.get_traced_memory()
    print(f"named tuples:\n  mem_current: {length_formatter(cur)}\n     mem_peak: {length_formatter(pk)}")
