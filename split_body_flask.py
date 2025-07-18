def split_body(body):
    data = body['data']
    mod = body['mod']
    question = body.get("question")
    return data,mod,question

