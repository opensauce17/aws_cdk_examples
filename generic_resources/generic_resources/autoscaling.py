import os
from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    # aws_sqs as sqs,
)
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_iam as iam
import aws_cdk.aws_cloudwatch as cloudwatch
from constructs import Construct

'''
Gather user data file
'''
with open(os.path.join("generic_resources", "user_data", "user-data.sh"), "r") as f:
    user_data = f.read()




class autoScaling(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        '''
        specify AMI in region
        '''
        amazon_linux_ami = ec2.GenericLinuxImage({
            # "eu-west-1": "ami-0c1bc246476a5572b"
            "us-east-1": self.node.try_get_context("ami")
        })

        alb = elb.ApplicationLoadBalancer(
            self, "AppLB", vpc=vpc, internet_facing=True, load_balancer_name="AppLB"
        )
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        listener = alb.add_listener("port80", port=80, open=True)

        self.asg = autoscaling.AutoScalingGroup(self, "ASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(
                                                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                                                instance_type=ec2.InstanceType(
                                                    instance_type_identifier=self.node.try_get_context("ec2_type")),
                                                machine_image=amazon_linux_ami,
                                                role=iam.Role.from_role_arn(self,
                                                                            "Role",
                                                                            self.node.try_get_context("asg_role"),
                                                                            mutable=False
                                                                            ),
                                                user_data=ec2.UserData.custom(
                                                    user_data),
                                                associate_public_ip_address=False,
                                                desired_capacity=self.node.try_get_context("asg_desired_capacity"),
                                                min_capacity=self.node.try_get_context("min_capacity"),
                                                max_capacity=self.node.try_get_context("max_capacity"),
                                                )

        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        CfnOutput(self, "Output", value=alb.load_balancer_dns_name)
