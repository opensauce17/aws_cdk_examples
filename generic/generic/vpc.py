# import aws_cdk as cdk
from aws_cdk import Stack
from constructs import Construct

import aws_cdk.aws_ec2 as ec2

'''
This class creates a generic VPC with context varibales listed in cdk.context.json. The VPC
will have public and private subnets spread over the chosen number of AZ's.
'''
class VpcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=self.node.try_get_context("max_azs"),
            cidr=self.node.try_get_context("cidr"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=self.node.try_get_context("pub_cidr_mask")
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    name="Private",
                    cidr_mask=self.node.try_get_context("pvt_cidr_mask"),
                ),
            ],
            nat_gateways=self.node.try_get_context("nat_gateways"),
        )

        aws_cdk.CfnOutput(self, "Output", value=self.vpc.vpc_id)