# Aira_V2_GPT
💡 요구사항 정리
	1.	현재 배포 상태
	•	프론트엔드(Frontend)와 백엔드(Backend) 서버를 각각 ECS (Elastic Container Service) 로 배포.
	•	각각의 서비스는 로드 밸런서(ALB) 를 통해 관리됨.
	•	데이터베이스는 MySQL 컨테이너 로 백엔드 내부에서 운영.
	2.	문제점
	•	OpenAI API 호출을 통해 대화가 이루어지는데, 현재는 백엔드가 프라이빗 네트워크 안에 있음.
	•	OpenAI API는 외부 서비스이므로, 프라이빗 네트워크에서는 호출할 수 없음 → 응답을 받지 못함.
	3.	해결책
	•	OpenAI API 호출을 담당하는 GPT Generate Endpoint 를 퍼블릭 네트워크로 이동.
	•	동시에 FIFO SQS (Simple Queue Service) 를 도입하여 트랜잭션 무결성을 보장.
	•	즉, OpenAI API 호출을 담당하는 별도의 컨테이너를 퍼블릭에 배치하여 호출 가능하게 하고, 이 호출이 SQS와 함께 관리되도록 개선.

📌 새로운 아키텍처의 주요 변경 사항
	•	백엔드 내부의 GPT 호출 로직을 분리하여 퍼블릭 환경에서 실행되는 GPT 컨테이너 로 이동.
	•	FIFO SQS 를 도입하여 트랜잭션 무결성을 확보.
	•	OpenAI API를 호출하는 부분은 퍼블릭 네트워크에 배치하여 접근 가능하도록 설정.
