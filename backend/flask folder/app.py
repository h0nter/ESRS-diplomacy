# from flask import Flask
# import requests

# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello, World!'

# @app.route('/post', methods=['GET'])
# def port_test():
#     url = "https://http://127.0.0.1:8000//graphql" 

#     body = """
#     query{ units {id} }
#     """

#     res = requests.post(url=url, json={"query": body})
#     print(res.text)
#     return "res.text"


# if __name__ == '__main__':
#       app.run(host='0.0.0.0', port=5173)