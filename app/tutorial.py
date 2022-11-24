from __future__ import print_function  # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key
from flask import render_template, url_for, redirect, request
from app import webapp

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tableName = 'Issues'


@webapp.route('/tutorial/create_table')
def tutorial_create_table():

    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': 'IssueId',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': "CreateDateIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'CreateDate'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'IssueId'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'INCLUDE',
                    'NonKeyAttributes': ['Description', 'Status']
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "TitleIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'Title'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'IssueId'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "DueDateIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'DueDate'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            }
        ],

        AttributeDefinitions=[
            {
                'AttributeName': 'IssueId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'CreateDate',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'DueDate',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    return redirect(url_for('tutorial'))


@webapp.route('/tutorial/delete_table')
def tutorial_delete_table():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    response = dynamodb.delete_table(
        TableName=tableName
    )

    return redirect(url_for('tutorial'))


def tutorial_putItem(issueId, title, description, createDate,
                     lastUpdateDate, dueDate, priority, status):

    table = dynamodb.Table(tableName)

    response = table.put_item(
        Item={
            'IssueId': issueId,
            'Title': title,
            'Description': description,
            'CreateDate': createDate,
            'LastUpdateDate': lastUpdateDate,
            'DueDate': dueDate,
            'Priority': priority,
            'Status': status
        }
    )

    return


@webapp.route('/tutorial/load_data')
def tutorial_load_data():

    print("Loading data into table " + tableName + "...")

    # IssueId, Title,
    # Description,
    # CreateDate, LastUpdateDate, DueDate,
    # Priority, Status

    tutorial_putItem("A-101", "Compilation error",
                     "Can't compile Project X - bad version number. What does this mean?",
                     "2017-04-01", "2017-04-02", "2017-04-10",
                     1, "Assigned")

    tutorial_putItem("A-102", "Can't read data file",
                     "The main data file is missing, or the permissions are incorrect",
                     "2017-04-01", "2017-04-04", "2017-04-30",
                     2, "In progress")

    tutorial_putItem("A-103", "Test failure",
                     "Functional test of Project X produces errors",
                     "2017-04-01", "2017-04-02", "2017-04-10",
                     1, "In progress")

    tutorial_putItem("A-104", "Compilation error",
                     "Variable 'messageCount' was not initialized.",
                     "2017-04-15", "2017-04-16", "2017-04-30",
                     3, "Assigned")

    tutorial_putItem("B-101", "Network issue",
                     "Can't ping IP address 127.0.0.1. Please fix this.",
                     "2017-04-15", "2017-04-16", "2017-04-19",
                     5, "Assigned")

    return redirect(url_for('tutorial'))


@webapp.route('/tutorial/list_all/<indexName>')
def tutorial_list_all(indexName):

    table = dynamodb.Table(tableName)

    response = table.scan(IndexName=indexName)

    records = []

    for i in response['Items']:
        records.append(i)

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            IndexName=indexName,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )

        for i in response['Items']:
            records.append(i)

    return render_template("tutorial/issues.html", issues=records)


@webapp.route('/tutorial/query_createdate')
def tutorial_query_createdate():
    try:
        table = dynamodb.Table(tableName)

        date = request.args.get('date')
        issue_id = request.args.get('issue_id')

        response = table.query(
            IndexName='CreateDateIndex',
            ##### Your code starts here #####



            ##### Your code ends here #####
        )

        records = []

        for i in response['Items']:
            records.append(i)

        return render_template("tutorial/issues.html", issues=records)
    except Exception as e:
        return str(e)


@webapp.route('/tutorial/query_title')
def tutorial_query_title():
    try:
        table = dynamodb.Table(tableName)
        title = request.args.get('title')

        response = table.query(
            IndexName='TitleIndex',
            ##### Your code starts here #####



            ##### Your code ends here #####
        )

        records = []

        for i in response['Items']:
            records.append(i)

        return render_template("tutorial/issues.html", issues=records)
    except Exception as e:
        return str(e)


@webapp.route('/tutorial/query_duedate')
def tutorial_query_duedate():
    try:
        table = dynamodb.Table(tableName)
        duedate = request.args.get('duedate')


        records = []
        return render_template("tutorial/issues.html", issues=records)
    except Exception as e:
        return str(e)
