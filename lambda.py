import boto3
import datetime
import json
import os
import time
import asyncio


'''
Create by sj kwon
2024-03-11
'''

def get_ssm_parameters_role(accountId):
    ssm_client = boto3.client('ssm');
    iam_role_arn=ssm_client.get_parameters(Names=['SCHEDUELR_IAM_ROLE_ARN'])['Parameters'];
    value=iam_role_arn[0]['Value']
    # using json.loads()
    # convert dictionary string to dictionary
    res = json.loads(value)
    print("IAM_ROLE_ARN : "+res[accountId])
    return res[accountId]
def get_ssm_parameters_svc():
    accountList=[]
    ssm_client = boto3.client('ssm');
    svc_name=ssm_client.get_parameters(Names=['SCHEDUELR_SVC'])['Parameters'];
    value=svc_name[0]['Value']
    # using json.loads()
    # convert dictionary string to dictionary
    res = json.loads(value)
    
    for i in res:
        if res[i] == "ON" :
            accountList.append(i) 
        else :
            continue
    
    return accountList
def getToken(accountId):
	SESSION_KEY={
    "aws_access_key_id":"",
        "aws_secret_access_key":"",
        "aws_session_token":""
	}

	sts_client=boto3.client('sts');
        #get session to target aws account.
	response = sts_client.assume_role(
    	RoleArn=get_ssm_parameters_role(accountId),
    	RoleSessionName="scheduler-session"
        )
        #set aws access config
	SESSION_KEY["aws_access_key_id"]=response['Credentials']['AccessKeyId']
	SESSION_KEY["aws_secret_access_key"]=response['Credentials']['SecretAccessKey']
	SESSION_KEY["aws_session_token"]=response['Credentials']['SessionToken']
    
	return SESSION_KEY;    

class Ec2:
	def __init__(self,token):
		self.ec2_client=boto3.client('ec2',aws_access_key_id=token["aws_access_key_id"],
        aws_secret_access_key=token["aws_secret_access_key"],
        aws_session_token=token["aws_session_token"]
        );

	def get_ec2_lists(self,SCH_TIME):
		sch_ec2_list=[]
		response=self.ec2_client.describe_instances(
			Filters = [
				{
					'Name' : 'tag:SCHEDUELR',
					'Values' : ['ON',]
				},
				{
					'Name' : 'tag:SCH_TIME',
					'Values' : [SCH_TIME,]
				}
			]
		);
	
		ec2_instances=response.get("Reservations")
		for i in range(len(ec2_instances)):
			sch_ec2_list.append(ec2_instances[0]['Instances'][0]['InstanceId']);
		print("##Schedule EC2 Lists###")			
		print(sch_ec2_list)		
		return sch_ec2_list

	def stop_ec2(self,instance_ids):
		response = self.ec2_client.stop_instances(
	    		InstanceIds=instance_ids)
		print(response)
		print('###{0} STOPT###'.format(instance_ids))
		
	def start_ec2(self,instance_ids):
		response = self.ec2_client.start_db_instance(
    			InstanceIds=instance_ids)
		print(response)
		print('###{0} START###'.format(instance_ids))

def lambda_handler(event, context):
	# TODO implement
	# 1. Scanning ALL EC2 ...
	# 2. Get EC2 Tags with SCHEDUELR
	# 3. if SCHEDUELR ON -> put rule stop or start rule
	SCH_TIME=event['SCH_TIME']
	sch_instnaces={}
	#accountList = ["AccountA","AccountB",...,]
	accountList=get_ssm_parameters_svc();


	for i in accountList:
		token = getToken(i);
		ec2=Ec2(token);
		#check schedule ec2
		#sch_instnaces = {'AccountA' : [instanceA,instanceB,instanceC,...,]		}
		sch_instnaces[i]=ec2.get_ec2_lists(SCH_TIME);
		
		if event['ACTION'] == "STOP":
			#ec2.stop_ec2(sch_instnaces[i]);
			print("Stop Instances")
		elif event['ACTION'] == "START" :
			#ec2.start_ec2(sch_instnaces[i]);
			print("Start Instances")
