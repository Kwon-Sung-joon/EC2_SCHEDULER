# EC2 스케줄러

AWS EC2 인스턴스의 시작과 중지를 자동화하는 스케줄러

## 동작 방식

1. SSM Parameter 생성
- SCHEDUELR_IAM_ROLE_ARN : 스케줄러를 실행 할 계정의 IAM Role (EC2 실행/중지 권한 및 Assume Role, Trust Advisor 설정 필요)
- SCHEDULER_SVC : 계정 별 스케줄러 ON OFF 지정


2. EventBridge Schedules 생성
- 원하는 시간에 대한 START , STOP 스케줄 생성

3. 대상 EC2 태그 추가
  - SCHEDUELR 태그 : ON/OFF 값 설정
  - SCH_TIME 태그 : 2번에서 생성한 스케줄러의 Payload 값과 동일하게 설정

