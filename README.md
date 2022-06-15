# flask-splitwise-example
An example Flask application to show the usage of Splitwise SDK

## Installation

Install requirements:

```sh
pip install -r requirements.txt
```

## Register your application [already done]

Goto [Splitwise](https://secure.splitwise.com/oauth_clients) and register you application. Use the following -

Homepage URL - http://localhost:5000 

Callback URL - http://localhost:5000/authorize

Make note of Consumer Key and Consumer Secret

## Set Configuraion

Open ```config.py``` and replace CONSUMER_KEY and CONSUMER_SECRET by the values you got after registering your application.

## Run the application

Goto the cloned repository and type 

```python
flask run
```

Goto http://localhost:5000/ on your browser.

## Contact
Contact naman (dot) aggarwal (at) yahoo (dot) com for any information.


