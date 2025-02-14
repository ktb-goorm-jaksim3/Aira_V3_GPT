import json
import time
import boto3
import openai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

sqs = boto3.client("sqs", region_name="ap-northeast-2")

REQUEST_QUEUE_URL = "https://sqs.ap-northeast-2.amazonaws.com/730335258114/gpt-request-queue.fifo"
RESPONSE_QUEUE_URL = "https://sqs.ap-northeast-2.amazonaws.com/730335258114/gpt-response-queue.fifo"

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=REQUEST_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )

        if "Messages" in response:
            for message in response["Messages"]:
                body = json.loads(message["Body"])
                request_id = body["request_id"]
                prompt = body["prompt"]

                # OpenAI API 호출
                openai_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )

                result = openai_response["choices"][0]["message"]["content"]

                # 결과를 SQS에 저장
                response_message = {"request_id": request_id, "result": result}
                sqs.send_message(
                    QueueUrl=RESPONSE_QUEUE_URL,
                    MessageBody=json.dumps(response_message)
                )

                # 처리된 메시지는 삭제
                sqs.delete_message(
                    QueueUrl=REQUEST_QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"]
                )

        time.sleep(2)

if __name__ == "__main__":
    process_messages()