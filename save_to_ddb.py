import os
import boto3
import json

from aws import dynamodb as table

def save_to_dynamodb():
    print("inside save_to_dbb")
    if os.path.exists("report.json") :
        print("path exists")
        with open('report.json') as testReport:
            results = json.load(testReport)
            report = results['report']
            tests = report['tests']
            time = report['created_at']
            name = tests[0]['name']
            outcome = tests[0]['outcome']
            # print(json.dumps(outcome, indent = 4, sort_keys=True))
            table.put_item(TableName = 'TestResults',
                Item={
                    'time' : {'S' : time},
                    'name' : {'S' : name},
                    'outcome' : {'S' : outcome}
                }
            )
            print("added to dynamodb")

        os.remove("report.json")
        print("removed json")
    print("out of path exists")

save_to_dynamodb()