# Python 3.5.2

import csv
import json
import multiprocessing
import logging
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('github_n_users.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

API_URL = "https://api.github.com"
STEP = 10 ** 5
MAX_N_USERS = 10 ** 6
CSV_FILE = 'n_users.csv'

def human_result(json_result):
    return json.dumps(json_result, indent=4)

def human_time(timestamp):
    date = datetime.fromtimestamp(int(timestamp), timezone.utc)
    return date.strftime('%Y-%m-%d %H:%M:%S %Z')

def write_csv(values, filename, mode='w'):
    if len(values) == 0 or type(values[0]) != dict:
        return
    # maintain keys order (for updating)
    keys = sorted(values[0].keys(), reverse=True)
    with open(filename, mode) as fname:
        writer = csv.DictWriter(fname, keys)
        if mode == 'w':
            writer.writeheader()
        writer.writerows(values)
 
def read_csv(filename):
    with open(csv_file) as fname:
        reader = csv.reader(fname)
        rows = list(reader)
        return rows
            
class ClientAPIGitHubv3:

    def __init__(self):
        self.access_token = 'a9a12f4e1c9ae97415a7397019c11696ac2383c0'

    def query(self, path, url=False, **params):
        params['access_token'] = self.access_token
        if not url:
            path = API_URL + path
        self.response = requests.get(path, params=params)
        self.request = self.response.request
        # r.headers['X-RateLimit-Limit']
        # r.headers['X-RateLimit-Remaining']
        # r.headers['X-RateLimit-Reset']
        return self.response.json()

    def rate_limit(self):
        return self.query('/rate_limit')

    def get_old_n_users(self, begin_id, end_id, step, csv_file):
        assert begin_id < end_id
        lower_bounds = range(begin_id, end_id, step)
        higher_bounds = range(step - 1, end_id + step, step)
        n_cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=n_cores)
        bounds = zip(lower_bounds, higher_bounds)
        last_users = pool.starmap(self.binary_search, bounds)
        last_users.insert(0, client.query('/users', since=0)[0])
        last_users = [self.parse_result(user) for user in last_users]
        write_csv(last_users, CSV_FILE)
        return self

    def get_n_users(self, step, csv_file):
        rows = read_csv(csv_file)
        last_n_users = int(rows[-1][0])
        last_user = self.binary_search(last_n_users, last_n_users + step)
        last_user = self.parse_result(last_user)
        write_csv([last_user], CSV_FILE, mode='a')
        return self

    def binary_search(self, first, last):
        last_user_id = first
        while first <= last:
            mid = (first + last) >> 1
            print(mid)
            users = self.query('/users', since=mid)
            if len(users) == 1:
                break
            elif len(users) > 1:
                first = mid + 1
            else:
                last = mid - 1
        return users[0]

    def parse_result(self, user):
        user = self.query(user['url'], url=True)
        return {'n_users': user['id'], 'date': user['created_at']}


if __name__ == "__main__":
    try:
        client = ClientAPIGitHubv3()
        #client.get_old_n_users(0, MAX_N_USERS, STEP, CSV_FILE)
        client.get_n_users(10 * STEP, CSV_FILE)
    except Exception as e:
        logger.error(e)
    logger.info('OK')
