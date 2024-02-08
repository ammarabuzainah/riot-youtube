
from googleapiclient.discovery import build

api_key = 'AIzaSyCmELp0znT7F2H9aaMbaVMB-g0aLrFJvZw'

youtube = build('youtube', 'v3',developerKey = api_key)


request = youtube.videos().list(
    part='snippet,statistics',
    id='MMnRdQwypkM'
)

response = request.execute()
print(response)
