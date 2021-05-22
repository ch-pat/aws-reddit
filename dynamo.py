import boto3
from boto3.dynamodb.conditions import Key, Attr


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


def query_table_by_title(query_string: str):
    table = get_posts_table()
    response = table.scan(
        FilterExpression=Attr('title').contains(query_string)
    )
    results = []
    items = response['Items']
    for item in items:
        url = item['url']
        name = item['name']
        num_comments = item['num_comments']
        title = item['title']
        timestamp = item['timestamp']
        subreddit = item['subreddit']
        row = [title, subreddit, url, num_comments, timestamp, name]
        results += [row]
    return results

if __name__ == "__main__":
    table = get_posts_table()
    print(table.creation_date_time)
