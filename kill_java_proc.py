import psutil
from tabulate import tabulate

def find_process_info(process_name):
    """Find all running instances of a process and their memory usage, username, and pid"""
    result = []
    for proc in psutil.process_iter(['name', 'memory_info', 'username', 'pid']):
        if proc.info['name'] == process_name:
            memory_usage_mb = round(proc.info['memory_info'].rss / (1024 * 1024), 2)  # convert bytes to MB
            result.append([proc.info['name'], proc.info['username'], proc.info['pid'], f'{memory_usage_mb} MB'])
    return result


process_name = 'java.exe'
process_instances = find_process_info(process_name)
if process_instances:
    table_headers = ['Process Name', 'Username', 'PID', 'Memory Usage']
    table_rows = []
    for process_info in process_instances:
        table_rows.append(process_info)
    print(tabulate(table_rows, headers=table_headers, tablefmt='plain', numalign='left'))
    pid_list = input(f'Enter the PIDs of the {process_name} instances to terminate (separated by commas): ')
    pid_list = pid_list.strip().split(',')
    pids_to_terminate = []
    for pid in pid_list:
        try:
            pid = int(pid)
            pids_to_terminate.append(pid)
        except ValueError:
            print(f'Error: "{pid}" is not a valid integer.')
    if pids_to_terminate:
        for pid in pids_to_terminate:
            try:
                psutil.Process(pid).terminate()
                print(f'{process_name} instance with PID {pid} has been terminated.')
            except psutil.NoSuchProcess:
                print(f'Error: No process with PID {pid} was found.')
else:
    print(f'{process_name} is not running.')
