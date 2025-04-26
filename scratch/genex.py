import tracemalloc

k = [i for i in range(100000)]

def sumsqg(m):
    tracemalloc.start()
    sq = (j*j for j in m)
    total = sum(sq)
    cur, pk = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tracemalloc.clear_traces()
    return (total, cur, pk)

def sumsql(m):
    tracemalloc.start()
    sq = [j*j for j in m]
    total = sum(sq)
    cur, pk = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tracemalloc.clear_traces()
    return (total, cur, pk)

print("genex", sumsqg(k))
print("list", sumsql(k))


# 1000
# genex (332833500, 228, 440)
# list (332833500, 40284, 40304)

# 10000
# genex (333283335000, 232, 440)
# list (333283335000, 404608, 404624)

# 100000
# genex (333328333350000, 232, 440)
# list (333328333350000, 4000416, 4000432)
