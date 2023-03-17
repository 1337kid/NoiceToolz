import random,base64,string,yaml

def generate_rand_id(size):
    chars=string.ascii_lowercase+string.ascii_uppercase+'0123456789'
    rid=''
    for i in range(size):
        rid+=random.choice(chars)
    return rid

def base64_dec_enc(data,enc):
    if enc==True:
        data=base64.b64encode(data.encode('utf-8')).decode('utf-8')
        return data
    else:
        data=base64.b64decode(data).decode('utf-8')
        return data
def read_yml(filename):
    with open(filename, mode="rb") as f:
        data = yaml.safe_load(f)
        return data