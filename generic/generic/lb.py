# import aws_cdk as cdk
from aws_cdk import Stack
from constructs import Construct

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb


class lbStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        alb = elb.ApplicationLoadBalancer(
            self, "AppLB", vpc=vpc, internet_facing=True, load_balancer_name="AppLB"
        )
        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Internet access ALB 80")
        listener = alb.add_listener("port80", port=80, open=True)

        cdk.CfnOutput(self, "Output", value=alb.load_balancer_dns_name)
