import requests
import datetime
import time
import config as cfg

last_ledger_seq = 0
last_ledger_time = 0
closing_times = []


# FUNCTION get_server_info()
# Get latest ledger sequence and timestamp from Rippled server
# Rippled Server URL defined in server_url
# Ledger Sequence Updated in last_ledger_seq
# Server Timestamp Updated in last_ledger_time
def call_server_info():
    global last_ledger_seq, last_ledger_time
    is_new_ledger = False
    rest_param = '{"method": "server_info"}'
    response = requests.post(cfg.server_url, data=rest_param)
    # if server response is OK
    if response.status_code == 200:
        server_info = response.json()
        curr_ledger_seq = server_info["result"]["info"]["validated_ledger"]["seq"]
        curr_ledger_time = datetime.datetime.strptime(server_info["result"]["info"]["time"], '%Y-%b-%d %H:%M:%S.%f %Z')
        ledger_closing_time = server_info["result"]['info']['last_close']['converge_time_s']

        # If received ledger sequence is not already in dictionary
        # Add it to dictionary and update last_ledger_seq to equal received ledger seq
        if int(curr_ledger_seq) != last_ledger_seq:
            # update latest fetched ledger seq and time values
            last_ledger_time = curr_ledger_time.strftime('%Y-%m-%d %H:%M:%S')
            last_ledger_seq = int(curr_ledger_seq)
            # print results for logging purposes
            print(f'{last_ledger_time}, {last_ledger_seq}')
            # log closing time for last ledger into list
            closing_times.append(ledger_closing_time)
            # mark this ledger as new
            is_new_ledger = True

    return is_new_ledger


# FUNCTION write_to_file()
# Write string line to file
# File path defined in ledger_file_path
def write_to_file(file_path, line):
    output = open(file_path, "a")
    output.write(line)
    output.close()


# FUNCTION print_closing_stats()
# Calculate the min, max and average time that it took for a new ledger to be validated
# Save stats in file path defined in stats_file_path
# BONUS 1 Question
def calc_closing_stats():
    count = len(closing_times)
    min_t = round(min(closing_times), 3)
    max_t = round(max(closing_times), 3)
    avg_t = round(sum(closing_times) / len(closing_times), 3)
    # save statistics results in file
    write_to_file(cfg.stats_file_path, cfg.stats_str.format(count, min_t, max_t, avg_t))
    # print results for logging purposes
    print(cfg.stats_str.format(count, min_t, max_t, avg_t))


# MAIN
# start polling process with an infinite loop
while True:
    try:
        # if New ledger fetched from server
        if call_server_info():
            # write ledger sequence and timestamp to file
            write_to_file(cfg.ledger_file_path, cfg.line_format.format(last_ledger_time, last_ledger_seq))
            # bonus question 1 results
            calc_closing_stats()

        # sleep till next run for sleep_time seconds
        time.sleep(cfg.sleep_time)
    except KeyboardInterrupt:
        print("Hard Exit Initiated. Goodbye!")
        break
