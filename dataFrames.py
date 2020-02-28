import os
import pandas as pd
import xlrd
import boto3
import json
import logging

from botocore.exceptions import ClientError

from aws import s3_client, dynamodb as table

import save_to_ddb as sdd

def create_data_frame():
    directory = 'Reports/'
    output = open('output.json', 'w')
    df = pd.DataFrame(columns = [
        'Contracting Company',
        'Labor Category',
        'Skill Level',
        'Clearance',
        'Location',
        'Position Description',
        'Skills',
        'Certifications',
        'Night Work',
        'Pager Duty',
        'Weekend Work',
        'Shift Work'
    ])

    if len(os.listdir(directory)) == 0 :
        return False

    for f in os.listdir(directory) :
        workbook = xlrd.open_workbook(directory + f)
        worksheet = workbook.sheet_by_index(0)
        cell1 =  worksheet.cell(1,0).value
        cell2 = worksheet.cell(6,0).value
        if 'Everest' in cell1 :
            for row in range(2, worksheet.nrows) :
                df = df.append(
                    {
                        'Contracting Company' : 'Everest',
                        'Labor Category' : worksheet.cell(row,6).value,
                        'Skill Level' : worksheet.cell(row,7).value,
                        'Clearance' : 'see Position Description',
                        'Location' : worksheet.cell(row,5).value,
                        'Position Description' : worksheet.cell(row,17).value,
                        'Mandatory Skills' : worksheet.cell(row,8).value,
                        'Desired Skills' : worksheet.cell(row,8).value,
                        'Certifications' : 'see Position Description',
                        'Night Work' : 'not provided',
                        'Pager Duty' : 'not provided',
                        'Weekend Work' : 'not provided',
                        'Shift Work' : 'not provided'
                    },
                    ignore_index = True
                )
        elif 'CSR' in cell1 :
            for row in range(2, worksheet.nrows) :
                df = df.append(
                    {
                        'Contracting Company' : 'GDIT',
                        'Labor Category' : worksheet.cell(row,1).value,
                        'Skill Level' : worksheet.cell(row,2).value,
                        'Clearance' : worksheet.cell(row,4).value,
                        'Location' : worksheet.cell(row,5).value,
                        'Position Description' : worksheet.cell(row,6).value,
                        'Mandatory Skills' : worksheet.cell(row,7).value,
                        'Desired Skills' : worksheet.cell(row,8).value,
                        'Certifications' : worksheet.cell(row,9).value,
                        'Night Work' : worksheet.cell(row,16).value,
                        'Pager Duty' : worksheet.cell(row,18).value,
                        'Weekend Work' : worksheet.cell(row,20).value,
                        'Shift Work' : worksheet.cell(row,21).value
                    },
                    ignore_index = True
                )
        elif 'JiTR' in cell2 :
            for row in range(6, worksheet.nrows) :
                df = df.append(
                    {
                        'Contracting Company' : 'Leidos',
                        'Labor Category' : worksheet.cell(row,3).value,
                        'Skill Level' : worksheet.cell(row,4).value,
                        'Clearance' : 'not provided',
                        'Location' : worksheet.cell(row,13).value,
                        'Position Description' : worksheet.cell(row,7).value,
                        'Mandatory Skills' : worksheet.cell(row,10).value,
                        'Desired Skills' : 'not provided',
                        'Certifications' : worksheet.cell(row,14).value,
                        'Night Work' : 'not provided',
                        'Pager Duty' : 'not provided',
                        'Weekend Work' : 'not provided',
                        'Shift Work' : 'not provided'
                    },
                    ignore_index = True
                )
    print(df.to_json(orient='records', lines=True), file=output)
    output.close()
    uploaded = upload_to_aws('output.json', 'kilpatrickprocessedbucket2')

    return True

def upload_to_aws(file_name, bucket, object_name=None):

    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print("file uploaded successfully")
    except ClientError as e:
        logging.error(e)
        return False

    return True

data_frame = create_data_frame()