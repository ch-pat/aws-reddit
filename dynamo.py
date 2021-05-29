import boto3
from boto3.dynamodb.conditions import Key, Attr
import os


TABLE_NAME = 'posts'

def get_posts_table():
    client = boto3.client('dynamodb')
    list_of_tables = client.list_tables()['TableNames']
    if TABLE_NAME in list_of_tables:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(TABLE_NAME)
        return table
    return create_posts_table()
    
def create_posts_table():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            },
            {
                "AttributeName": "timestamp",
                "KeyType": "RANGE"
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table


def query_table_by_title(query_string: str, subreddit: str):
    table = get_posts_table()
    response = table.query(
        IndexName='subreddit-timestamp-index',
        KeyConditionExpression=Key('subreddit').eq(subreddit),
        FilterExpression=Attr('title').contains(query_string)
    )
    results = []
    items = response['Items']
    for item in items:
        url = item['url']
        name = item['name']
        title = item['title']
        timestamp = item['timestamp']
        subreddit = item['subreddit']
        row = [title, subreddit, url, timestamp, name]
        results += [row]
    return results

def default_query():
    table = get_posts_table()
    response = table.scan(
        Limit=20
    )
    results = []
    items = response['Items']
    for item in items:
        url = item['url']
        name = item['name']
        title = item['title']
        timestamp = item['timestamp']
        subreddit = item['subreddit']
        row = [title, subreddit, url, timestamp, name]
        results += [row]
    return results


def get_subreddit_counts():
    if os.path.isfile('subreddit_counts'):
        with open('subreddit_counts', 'r', encoding='utf-8') as f:
            results = f.readlines()

        return [r[:-1] for r in results]

    subredditss = subreddits()
    i = 0
    sub_counts = []
    for subreddit in subredditss:
        i += 1
        print(i)
        results = query_table_by_title('', subreddit)
        sub_counts += [f"{subreddit} {len(results)}\n"]
    with open('subreddit_counts', 'w+', encoding='utf-8') as f:
        f.writelines(sub_counts)

def subreddits() -> list:
    if os.path.isfile('subreddits'):
        with open('subreddits', 'r', encoding='utf-8') as f:
            results = f.readlines()

        return [r[:-1] for r in results]
    else:
        table = get_posts_table()
        results = []
        items = []
        last_evaluated_key = None

        # Get all items from DB !!! takes a long time !!!
        while True:
            if last_evaluated_key:
                response = table.scan(
                    ExclusiveStartKey=last_evaluated_key
                )
            else: 
                response = table.scan()
            last_evaluated_key = response.get('LastEvaluatedKey')
            
            items.extend(response['Items'])
            
            if not last_evaluated_key:
                break
        ######


        for item in items:
            subreddit = f"{item['subreddit']}\n"
            if subreddit not in results:
                results += [subreddit]
        results = sorted(results)
        with open('subreddits', 'w+', encoding='utf-8') as f:
            f.writelines(results)
        return results

if __name__ == "__main__":
    table = get_posts_table()
    print(table.creation_date_time)
