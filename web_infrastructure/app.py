#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from webserver_infra.network_stack import prdVpcStack, devVpcStack
from webserver_infra.ec2_compute_stack import prdEc2Stack, devEc2Stack
from webserver_infra.rds_compute_stack import prdRdsStack, devRdsStack

'''
Import and define configuration variables
'''
from webserver_infra.config.config_reader import config_json_read 
data = config_json_read()
dev_acc = data["env"]["dev"]["account"]
dev_region = data["env"]["dev"]["region"]
prd_acc = data["env"]["prd"]["account"]
prd_region = data["env"]["prd"]["region"]

app = cdk.App()


'''
Define the accounts and environments
'''
dev_env_FRA = cdk.Environment(account=dev_acc, region=dev_region)
prd_env_IRE = cdk.Environment(account=prd_acc, region=prd_region)
'''
Instantiate the development and production VPC/Network stacks
'''
dev_vpc_stack = devVpcStack(app, "dev-network", env=dev_env_FRA)
prd_vpc_stack = prdVpcStack(app, "prd-network", env=prd_env_IRE)

'''
Instantiate development and production EC2 Compute stacks
'''
dev_ec2_stack = devEc2Stack(app, "dev-ec2-compute", env=dev_env_FRA,
                            vpc=dev_vpc_stack.vpc)
prd_ec2_stack = prdEc2Stack(app, "prd-ec2-compute", env=prd_env_IRE,
                           vpc=prd_vpc_stack.vpc)
'''
Instantiate the development and production RDS Compute stacks
'''
dev_rds_stack = devRdsStack(app, "dev-rds-compute", env=dev_env_FRA,
                            vpc=dev_vpc_stack.vpc,
                            asg_security_groups=dev_ec2_stack.asg.connections.security_groups)
prd_rds_stack = prdRdsStack(app, "prd-rds-compute", env=prd_env_IRE,
                            vpc=prd_vpc_stack.vpc,
                            asg_security_groups=prd_ec2_stack.asg.connections.security_groups)

app.synth()
