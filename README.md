# EC2 스케줄러

AWS EC2 인스턴스의 시작과 중지를 자동화하는 스케줄러입니다. 이 스케줄러는 특정 시간에 EC2 인스턴스를 시작하거나 중지하도록 설정할 수 있습니다.

## 동작 방식

1. **SSM Parameter 생성**
   - **`SCHEDUELR_IAM_ROLE_ARN`**: 스케줄러를 실행할 계정의 IAM Role ARN. 이 Role은 EC2 인스턴스를 실행 및 중지할 수 있는 권한과 Assume Role을 수행할 수 있는 Trust Policy가 필요합니다.
   - **`SCHEDULER_SVC`**: 각 계정별 스케줄러의 ON/OFF 상태를 지정합니다. 이 값에 따라 스케줄러가 작동할 계정을 선택합니다.

2. **EventBridge Schedules 생성**
   - 원하는 시간에 대한 START 및 STOP 스케줄을 생성합니다. 이 스케줄은 EC2 인스턴스를 자동으로 시작하거나 중지하는 데 사용됩니다.

3. **대상 EC2 태그 추가**
   - **`SCHEDUELR` 태그**: 각 EC2 인스턴스에 ON 또는 OFF 값을 설정합니다. 이 값이 ON일 때만 스케줄러가 해당 인스턴스를 제어합니다.
   - **`SCH_TIME` 태그**: 2번에서 생성한 스케줄의 Payload 값과 동일하게 설정하여, 인스턴스가 언제 시작하거나 중지될지를 결정합니다.

## 사용 방법

1. **SSM Parameters 설정**
   - AWS SSM Parameter Store에 위에서 언급한 두 가지 Parameter를 생성합니다.

2. **EventBridge Rule 설정**
   - EC2 인스턴스의 시작 및 중지를 위한 EventBridge Rule을 설정합니다. 이 Rule은 지정된 시간에 Lambda 함수를 트리거합니다.

3. **Lambda 함수 배포**
   - 위의 코드를 AWS Lambda에 배포합니다. Lambda 함수는 EventBridge에 의해 트리거되어 EC2 인스턴스를 제어합니다.

4. **EC2 인스턴스 태그 설정**
   - 관리할 EC2 인스턴스에 `SCHEDUELR` 및 `SCH_TIME` 태그를 추가합니다.

## 코드 설명

- **get_ssm_parameters_role**: SSM에서 IAM Role ARN을 가져옵니다.
- **get_ssm_parameters_svc**: SSM에서 각 계정별 스케줄러의 ON/OFF 상태를 가져옵니다.
- **getToken**: 지정된 계정 ID로 Assume Role을 수행하여 AWS 인증 정보를 가져옵니다.
- **Ec2 클래스**: EC2 인스턴스의 시작 및 중지를 담당하는 메소드를 포함합니다.
  - **get_ec2_lists**: 지정된 스케줄 시간에 따라 EC2 인스턴스를 조회합니다.
  - **stop_ec2**: 인스턴스를 중지합니다.
  - **start_ec2**: 인스턴스를 시작합니다.
- **lambda_handler**: Lambda 함수의 진입점으로, EC2 인스턴스를 스케줄에 따라 시작하거나 중지합니다.

## 참고 자료

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS Systems Manager](https://aws.amazon.com/systems-manager/)
- [AWS EC2](https://aws.amazon.com/ec2/)
- [AWS EventBridge](https://aws.amazon.com/eventbridge/)
