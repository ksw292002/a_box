import boto3


# 유저이름을 받아서, 해당 유저의 이름을 포함한 테이블 생성
def createFileList(username) :
        
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName=username,
        KeySchema=[
            {
                'AttributeName': 'f_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'f_url',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'f_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'f_url',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )


    # Wait until the table exists.
    print("Wating for creating table")
    table.meta.client.get_waiter('table_exists').wait(TableName=username)

    # Print out some data about the table.
    print("Table created")
    print("count :")
    print(table.item_count)

# 유저이름을 받아서, 해당 유저의 file list에 받아온 file 이름과 그 url을 업데이트
def updateFileInfo(username, fname, furl) :
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(username)

    table.put_item(
    Item={
            'f_name': fname,
            'f_url': furl,
        }
    )