from __future__ import print_function # Python 2/3 compatibility
import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

from flask import render_template, url_for, redirect, request
from app import webapp

#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@webapp.route('/create_table')
def create_table():

    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    return redirect(url_for('lecture'))


@webapp.route('/delete_table')
def delete_table():
    #dynamodb = boto3.client('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    response = dynamodb.delete_table(
        TableName='Movies'
    )

    return redirect(url_for('lecture'))




@webapp.route('/put')
def movie_put():
    table = dynamodb.Table('Movies')

    title = request.args.get('title')
    year = int(request.args.get('year'))
    rating = request.args.get('rating')

    response = table.put_item(
       Item={
            'year': year,
            'title': title,
            'plot':"Nothing happens at all.",
            'rating': rating
        }
    )

    return redirect(url_for('lecture'))

@webapp.route('/get')
def movie_get():
    table = dynamodb.Table('Movies')

    title = request.args.get('title')
    year = int(request.args.get('year'))

    response = table.get_item(
       Key={
            'year': year,
            'title': title
        },
        ProjectionExpression = "#yr, title, rating, actors[0], genres",
        ExpressionAttributeNames = {"#yr": "year"}
    )

    data = {}

    if 'Item' in response:
        item = response['Item']
        data.update(item)

    return render_template("lecture/movie_detail.html", movie=data)


@webapp.route('/update')
def movie_update():
    table = dynamodb.Table('Movies')

    title = request.args.get('title')
    year = int(request.args.get('year'))
    rating = request.args.get('rating')


    response = table.update_item(
       Key={
            'year': year,
            'title': title
        },
        UpdateExpression = "set rating = :r, plot=:p, actors=:a",
        ExpressionAttributeValues = {
           ':r': rating,
           ':p': "Everything happens all at once.",
           ':a': ["Larry", "Moe", "Curly"]
        }

    )

    return redirect(url_for('lecture'))




@webapp.route('/import_data')
def import_data():


    table = dynamodb.Table('Movies')

    with open("moviedata.json") as json_file:
        movies = json.load(json_file)
        for movie in movies:
            year = int(movie['year'])
            title = movie['title']
            info = movie['info']

            print("Adding movie:", year, title)

            item = {
                'year': year,
                'title': title
            }

            item.update(info)

            table.put_item(
               Item = item
            )

    return redirect(url_for('lecture'))


@webapp.route('/list_all')
def list_all():

    table = dynamodb.Table('Movies')

    fe = Key('year').between(1950, 1959);
    pe = "#yr, title, rating"
    # Expression Attribute Names for Projection Expression only.
    ean = { "#yr": "year", }
    esk = None

    # FilterExpression=fe,

    response = table.scan(
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
        )

    records = []

    for i in response['Items']:
        records.append(i)

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=pe,
            ExpressionAttributeNames= ean,
            ExclusiveStartKey=response['LastEvaluatedKey']
            )

        for i in response['Items']:
            records.append(i)

    return render_template("lecture/movies.html", movies=records)

@webapp.route('/movies')
def movies_year():
    table = dynamodb.Table('Movies')

    if 'year' not in request.args or\
        request.args.get('year').isdigit() == False:
        return "Error! All inputs most be of type int"

    year = int(request.args.get('year'))

    response = table.query(
        KeyConditionExpression=Key('year').eq(year)
    )

    records = []

    for i in response['Items']:
        records.append(i)

    return render_template("lecture/movies.html", movies=records)

@webapp.route('/movies_year_title')
def movies_year_title():
    table = dynamodb.Table('Movies')

    year = int(request.args.get('year'))
    title_from = request.args.get('title_from')
    title_to = request.args.get('title_to')

    response = table.query(
        ProjectionExpression="#yr, title, rating",
        ExpressionAttributeNames={"#yr": "year"},  # Expression Attribute Names for Projection Expression only.
        KeyConditionExpression=Key('year').eq(year) & Key('title').between(title_from, title_to)
    )

    records = []

    for i in response['Items']:
        records.append(i)

    return render_template("lecture/movies.html", movies=records)
