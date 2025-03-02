import subprocess

def get_processes():
    # Get process info using ps command
    ps_command = [
        'ps',
        '-eo',
        'pid,user,%cpu,%mem,args',  # Select columns: PID, USER, %CPU, %MEM, COMMAND
    ]
    try:
        output = subprocess.check_output(ps_command, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing ps command: {e}")
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
    print(f"\n{'=' * 40}")
    print(f"Processes sorted by {title} (descending)")
    print(f"{'=' * 40}")
    print(f"{'PID':>7} {'USER':<10} {'CPU%':>6} {'MEM%':>6} COMMAND")
    for p in processes:
        print(f"{p['pid']:>7} {p['user']:<10} {p[sort_key]:>6.1f}% {p['mem']:>6.1f}% {p['cmd'][:80]}")

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
