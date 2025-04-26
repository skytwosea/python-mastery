import tracemalloc
import sys
from typing import Callable
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)

from Work.reader import *

assert isinstance(read_csv_as_columns, Callable)


pf_converter = [str, int, float]
tracemalloc.start()
pf_data = read_csv_as_columns("Data/portfolio.csv", pf_converter)
cur, pk = tracemalloc.get_traced_memory()
print(f"portfolio: cur={cur}, pk={pk}")
tracemalloc.stop()
tracemalloc.clear_traces()


cta_converter = [str, str, str, int]
tracemalloc.start()
cta_data = read_csv_as_columns("Data/ctabus.csv", cta_converter)
cur, pk = tracemalloc.get_traced_memory()
print(f"cta: cur={cur}, pk={pk}")
tracemalloc.stop()
tracemalloc.clear_traces()


cached_cta_converter = [sys.intern, str, str, int]
tracemalloc.start()
cta_cached = read_csv_as_columns("Data/ctabus.csv", cached_cta_converter)
cur, pk = tracemalloc.get_traced_memory()
print(f"cached_cta: cur={cur}, pk={pk}")
tracemalloc.stop()
tracemalloc.clear_traces()
