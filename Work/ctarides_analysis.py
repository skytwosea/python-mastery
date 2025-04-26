# shape of the source file:
#
# route , date       , daytype , rides
# 3     , 01/01/2001 , U       , 7354
# 4     , 01/01/2001 , U       , 9288
# ...
#
# silly americans; it's using mm/dd/yyyy

"""
Goal is to answer the following:

(1) how many bus routes in CTA?
    - should be length of deduplicated route column

(2) how many people rode route 22 on Feb 22, 2011 (or any given date)?
    - filter for date first, then for route, then sum rides

(3) what is total number of rides taken on each bus route?
    - group by route, then sum each group

(4) what five routes had greatest ten-year ridership increase from 2001-2011?
    - filter by date, then group by route, then get delta(max - min) for rides, then sort by rides delta
"""

FPATH = "Data/ctabus.csv"

from readrides import *
import time
from collections import Counter, defaultdict

def read_rides(filename, fn_key) -> list:
    # functionality like create_object and its attendant logic
    # are in module readrides, from prev. exercise
    # t0 = time.monotonic()
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
    # t1 = time.monotonic()
    # cur, pk = tracemalloc.get_traced_memory()
    # runtime = t1 - t0
    return records

def main():
    records = read_rides(FPATH, "slotted_dataclass")

    # (1)
    routes_count = {record.route for record in records}
    # print(f"Routes count: {len(routes_count)}")
    assert len(routes_count) == 181

    # (2)
    query_date = "02/02/2011"
    query_route = "22"
    routes_on_date = sum([
        record.rides for record in records
        if record.date == query_date and record.route == query_route
    ])
    # print(f"Rides on route {query_route} on {query_date}: {routes_on_date}")
    assert routes_on_date == 5055

    # (3)
    per_route = Counter()
    for record in records:
        per_route[record.route] = per_route.get(record.route, 0) + record.rides
    # for k,v in dict(sorted(per_route.items(), key=lambda item: item[1])).items():
    #     print(f"{k:<5}: {v}")
    assert per_route['79'] == 133796763
    assert per_route['9'] == 117923787
    assert per_route['49'] == 95915008


    # (4)
    in_date_range = [record for record in records if record.date[-4:] == "2001" or record.date[-4:] == "2011"]
    per_route_by_date = defaultdict(int)
    for record in in_date_range:
        per_route_by_date[f"{record.route}_{record.date[-4:]}"] += record.rides
    # print(per_route_by_date)
    delta = {}
    for route in routes_count:
        delta[route] = per_route_by_date[f"{route}_2011"] - per_route_by_date[f"{route}_2001"]
    # for k,v in dict(sorted(delta.items(), key=lambda item: item[1], reverse=True)).items():
    #     print(f"{k:10}: {v}")
    assert delta['15'] == 2732209
    assert delta['147'] == 2107910
    assert delta['66'] == 1612958
    assert delta['12'] == 1612067
    assert delta['14'] == 1351308





if __name__ == "__main__":
    main()
