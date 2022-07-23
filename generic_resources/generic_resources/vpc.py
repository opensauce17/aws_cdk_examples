from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    # aws_sqs as sqs,
)
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

'''
This class creates a generic VPC with context varibales listed in cdk.json. The VPC
will have public and private subnets spread over the chosen number of AZ's.
'''

class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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

        CfnOutput(self, "Output", value=self.vpc.vpc_id)