import re
import argparse
from collections import defaultdict
import pymysql

def analyze_apache_log(log_path):
    pattern = re.compile(r'^(\S+) (\S+) (\S+) \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)')
    url_stats = defaultdict(lambda: {'count': 0, 'status_codes': defaultdict(int)})

    try:
        with open(log_path, 'r') as f:
            for line in f:
                match = pattern.match(line)
                if match:
                    groups = match.groups()
                    url = groups[5]
                    status_code = groups[7]
                    
                    if 'index.php' in url:
                        url_stats[url]['count'] += 1
                        url_stats[url]['status_codes'][status_code] += 1

        print("Apache Log Analysis for index.php Requests:")
        print("{:<80} {:<10} {:<15}".format('URL', 'Total Hits', 'Status Codes'))
        for url, data in sorted(url_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:20]:
            status_str = ', '.join([f'{k}:{v}' for k, v in data['status_codes'].items()])
            print("{:<80} {:<10} {:<15}".format(url, data['count'], status_str))
            
    except FileNotFoundError:
        print(f"Error: Log file {log_path} not found")

def check_mysql_processes(mysql_user, mysql_password):
    try:
        connection = pymysql.connect(
            host='localhost',
            user=mysql_user,
            password=mysql_password,
            database='information_schema',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SHOW FULL PROCESSLIST")
            processes = cursor.fetchall()
            
            print("\nActive MySQL Processes:")
            print("{:<8} {:<12} {:<6} {:<12} {:<60}".format(
                'ID', 'User', 'Time', 'State', 'Query'
            ))
            for p in processes:
                if p['Command'] != 'Sleep' and p['Info'] is not None:
                    print("{:<8} {:<12} {:<6} {:<12} {:<60}".format(
                        p['Id'], p['User'], p['Time'], p['State'], p['Info'][:55]
                    ))
                    
    except pymysql.Error as e:
        print(f"MySQL Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diagnose PHP/MySQL performance issues')
    parser.add_argument('--log', help='Path to Apache access log')
    parser.add_argument('--mysql-user', help='MySQL username')
    parser.add_argument('--mysql-password', help='MySQL password')
    args = parser.parse_args()

    if args.log:
        analyze_apache_log(args.log)
        
    if args.mysql_user and args.mysql_password:
        check_mysql_processes(args.mysql_user, args.mysql_password)
    elif args.mysql_user or args.mysql_password:
        print("Error: Both --mysql-user and --mysql-password are required for MySQL check")
