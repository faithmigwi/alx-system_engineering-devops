#!/usr/bin/python3
"""
Python script that, using a REST API, for a given employee ID,
returns information about his/her TODO list progress and exports
the data to a CSV file.
"""

import requests
import csv
from sys import argv

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: {} <employee_id>".format(argv[0]))
        exit(1)

    base_url = 'https://jsonplaceholder.typicode.com/'
    todos_url = base_url + 'todos'
    users_url = base_url + 'users/{}'.format(argv[1])

    user_response = requests.get(users_url)
    user_data = user_response.json()

    todos_response = requests.get(todos_url, params={'userId': argv[1]})
    todos_data = todos_response.json()

    employee_id = user_data.get('id')
    employee_name = user_data.get('username')

    csv_file_name = '{}.csv'.format(employee_id)

    with open(csv_file_name, mode='w', newline='') as csvfile:
        fieldnames = ['USER_ID', 'USERNAME', 'TASK_COMPLETED_STATUS', 'TASK_TITLE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for task in todos_data:
            writer.writerow({
                'USER_ID': employee_id,
                'USERNAME': employee_name,
                'TASK_COMPLETED_STATUS': str(task.get('completed')),
                'TASK_TITLE': task.get('title')
            })

    print("Data exported to {}".format(csv_file_name))

