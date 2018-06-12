import boto3


# username 받아서 해당 이름의 bucket을 만든다.
def createUserBucket(username) :
    # Boto 3 - S3
    s3 = boto3.resource('s3')

    bname = 's3b'+str(username)
    s3.create_bucket(Bucket=bname, CreateBucketConfiguration={
        'LocationConstraint': 'us-west-2'})


# form으로 받아온 file name과 url을 이용하여 S3에 업로드.
def uploadFile(username, fname, furl) :
    
    # Boto 3 - S3
    s3 = boto3.resource('s3')

    bname = 's3b'+str(username)

    # bname이라는 이름을 가진 버킷에 fname으로 저장.
    # 세부 정보는 뒤에...
    s3.Object(bname, fname).put(Body=open(furl, 'rb'))


# username과 file name을 받아서 파일의 public url을 얻어온다.
# def getFileUrl(username, fname) :
    
#     bname = 's3b'+str(username)
#     url = '{}/{}/{}'.format('http://s3-us-west-2.amazonaws.com', bname, fname)

#     return url

def getFileUrl(username, fname) :
    # Get the service client.
    s3 = boto3.client('s3')

    bname = 's3b'+str(username)

    # Generate the URL to get 'key-name' from 'bucket-name'
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bname,
            'Key': fname
        }
    )

    return url

# username을 받아서 user가 가지고 있는 파일 리스트를 가져옴.
def getFileList(username):
    s3 = boto3.client('s3')

    """Get a list of keys in an S3 bucket."""
    keys = []
    bname = 's3b'+str(username)
    resp = s3.list_objects_v2(Bucket=bname)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys