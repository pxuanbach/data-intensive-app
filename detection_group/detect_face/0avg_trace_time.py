f = open("0logs.log", "r")
total_trace_time = 0
count_trace_time = 0
for i in f:
    if i.__contains__("Trace time"):
        str_arr = i.split(" ")
        trace_time = float(str_arr[len(str_arr)-2])
        total_trace_time += trace_time
        count_trace_time += 1

avg_trace_time = total_trace_time/count_trace_time
print("AVG", avg_trace_time)
print("TOTAL", total_trace_time)