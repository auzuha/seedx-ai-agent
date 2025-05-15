import os
import datetime
import json

def log_msg_to_file(log):
        today = str(datetime.date.today())
        fpath = f'./logs/{today}.json'
        if not os.path.exists(fpath):
            with open(fpath, 'w') as f:
                json.dump([log], f, indent=2)
        else:
            with open(fpath, 'r') as f:
                logs = json.load(f)
            logs.append(log)
            with open(fpath, 'w') as f:
                json.dump(logs, f, indent=2)