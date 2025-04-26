from typing import Callable
import csv
import collections

class CustomData(collections.abc.Sequence):
    def __init__(self, header: list):
        self.header = header
        self.cols = [
            [] for _ in range(len(header))
        ]

    def __len__(self):
        assert all(
            len(self.cols[n]) == len(self.cols[0])
            for n in range(len(self.cols))
        )
        return len(self.cols[0])

    def __getitem__(self, idx: int|slice):
        if isinstance(idx, int):
            return {
                self.header[n] : self.cols[n][idx] for n in range(len(self.cols))
            }
        elif isinstance(idx, slice):
            rtn_ = []
            _start = idx.start if idx.start else 0
            _stop = idx.stop if idx.stop else 0
            _step = idx.step if idx.step else 1
            assert _step != 0
            for i in range(_start, _stop, _step):
                rtn_.append(
                    { self.header[n] : self.cols[n][i] for n in range(len(self.header)) }
                )
            return rtn_
        else:
            return NotImplemented

    def append(self, d: dict):
        for k,v in d.items():
            idx_ = self.header.index(k)
            self.cols[idx_].append(v)

def read_csv_as_columns(fname: str, converter: list[Callable]) -> list[dict[str, str|int|float]]:
    with open(fname, 'r') as f:
        rows = csv.reader(f)
        headers = next(rows)
        rtn_ = CustomData(headers)
        for row in rows:
            rtn_.append(
                {
                    name:fn(val) for name, fn, val in zip(headers, converter, row)
                }
            )
    return rtn_
    
