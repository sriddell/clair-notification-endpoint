from flask import Flask, request
import json
import os
import boto3
import requests
app = Flask(__name__)

# @app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
# @app.route('/<path:path>', methods=['GET', 'POST'])
# def catch_all(path):
#     print(request)
#     print(request.data)
#     return 'You want path: %s' % path


@app.route('/notify', methods=['POST'])
def notify():
    payload = json.loads(request.data)
    id = payload['Notification']['Name']
    endpoint = None
    if 'SQS_ENDPOINT' in os.environ:
        endpoint = os.environ['SQS_ENDPOINT']
        print('using endpoint ' + endpoint)
    sqs = boto3.resource('sqs', region_name=os.environ['REGION'], endpoint_url=endpoint)
    queue = sqs.Queue(os.environ['SQS_QUEUE_URL'])
    msg = {'HandleNotification': {'name': id}}
    print("Queing msg:" + json.dumps(msg))
    queue.send_message(
        MessageBody=json.dumps(msg)
    )
    delete_notification(id)
    return ""


def delete_notification(notification_id):
    url = os.environ["CLAIR_ENDPOINT"] + '/v1/notifications/' + str(notification_id)
    resp = requests.delete(url)
    if not (resp.status_code == 200 or resp.status_code == 202 or resp.status_code == 204):
        print('Unable to delete ' + notification_id)
    else:
        print('DELETED ' + notification_id)


if __name__ == '__main__':
    app.run()
