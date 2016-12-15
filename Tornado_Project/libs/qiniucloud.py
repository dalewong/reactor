#coding:utf-8

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config


#需要填写你的 Access Key 和 Secret Key
access_key = 'fXQ5vNcbuZfheQdspaAcE6Ga1UwUMQX4YWLW2UbX'
secret_key = 'ZMOR5MpGn5Z-eVppjZ97A1Sc6xEAp3s6k3wXUGOp'

def avatarSave(data):
#构建鉴权对象
    q = Auth(access_key, secret_key)
    
    #要上传的空间
    bucket_name = 'dalewong'

    #上传到七牛后保存的文件名
    key = None

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_data(token, key, data)
    
    return ret['key']
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)
if __name__ == "__main__":
    # path = raw_input('请填写路径')
    path = '/Users/wangye/Desktop/chicken.jpg'
    with open(path, "rb") as f:
        file = f.read()
        avatarSave(file)