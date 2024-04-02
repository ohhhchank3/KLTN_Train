

from mediafire import MediaFireApi
from mediafire import MediaFireUploader
api = MediaFireApi()
uploader = MediaFireUploader(api)
session = api.user_get_session_token(
    email='20133118@student.hcmute.edu.vn',
    password='123456789@A',
    app_id='42511')

api.session = session
response = api.user_get_info()
fd = open(r"C:\Users\Admin\Downloads\demo2\tmp\demo.docx", 'rb')
result = uploader.upload(fd, 'demo1.docx',
                         folder_key='FOLDER KEY')