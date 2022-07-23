#!/usr/bin/env python3
import os
import aws_cdk as cdk

from generic_resources.vpc import VpcStack
from generic_resources.autoscaling import autoScaling
from generic_resources.rds import rdsMysql

app = cdk.App()

vpc_stack = "vpc-03734b2d1500358e9"

env_US = cdk.Environment(account="966348485303", region="us-east-1")

vpc_stack = VpcStack(app, "vpc", env=env_US)
as_stack = autoScaling(app, "auto-scale", vpc=vpc_stack.vpc, env=env_US)
rds_stack = rdsMysql(app, "rds", vpc=vpc_stack.vpc, asg_security_groups=as_stack.asg.connections.security_groups, env=env_US)

app.synth()
