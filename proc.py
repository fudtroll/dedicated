import subprocess

def get_processes():
    # Get process info using ps command
    ps_command = [
        'ps',
        '-eo',
        'pid,user,%cpu,%mem,args',  # Select columns: PID, USER, %CPU, %MEM, COMMAND
    ]
    try:
        output = subprocess.check_output(ps_command, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print("Error executing ps command: {}".format(e))
        return []

    lines = output.splitlines()
    if not lines:
        return []

    # Parse processes (skip header)
    processes = []
    for line in lines[1:]:
        parts = line.split(maxsplit=4)
        if len(parts) < 5:
            continue

        try:
            process = {
                'pid': parts[0],
                'user': parts[1],
                'cpu': float(parts[2]),
                'mem': float(parts[3]),
                'cmd': parts[4]
            }
            processes.append(process)
        except ValueError:
            continue  # Skip invalid entries

    return processes

def print_processes(processes, sort_key, title):
    print("\n{}".format('=' * 40))
    print("Processes sorted by {} (descending)".format(title))
    print("{}".format('=' * 40))
    print("{:>7} {:<10} {:>6} {:>6} COMMAND".format('PID', 'USER', 'CPU%', 'MEM%'))
    for p in processes:
        print("{:>7} {:<10} {:6.1f}% {:6.1f}% {}".format(
            p['pid'], 
            p['user'], 
            p[sort_key], 
            p['mem'], 
            p['cmd'][:80]
        ))

def main():
    processes = get_processes()
    
    if not processes:
        print("No processes found")
        return

    # Sort processes
    sorted_cpu = sorted(processes, key=lambda x: x['cpu'], reverse=True)
    sorted_mem = sorted(processes, key=lambda x: x['mem'], reverse=True)

    # Display results
    print_processes(sorted_cpu, 'cpu', 'CPU usage')
    print_processes(sorted_mem, 'mem', 'Memory usage')

if __name__ == "__main__":
    main()
