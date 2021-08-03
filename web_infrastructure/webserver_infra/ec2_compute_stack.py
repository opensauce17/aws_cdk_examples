import os
from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_iam as iam
import aws_cdk.aws_cloudwatch as cloudwatch

from config.config_reader import config_json_read
data = config_json_read()
dev_ec2_type = data["ec2_instance_size"]["dev"]
prd_ec2_type = data["ec2_instance_size"]["prd"]
dev_role = data["role_name"]["dev"]
prd_role = data["role_name"]["prd"]
dev_ami = data["ami_images"]["dev"]["eu-central-1"]
prd_ami = data["ami_images"]["prd"]["eu-west-1"]

linux_ami = ec2.GenericLinuxImage({
    "eu-central-1": dev_ami, 
    "eu-west-1": prd_ami
})

with open(os.path.join("webserver_infra", "user_data", "user-data.sh"), "r") as f:
    user_data = f.read()


class prdEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        alb = elb.ApplicationLoadBalancer(self, "AppLB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="AppLB"
                                         )
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        listener=alb.add_listener("port80",
                                  port=80,
                                  open=True)

        self.asg = autoscaling.AutoScalingGroup(self, "ASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=prd_ec2_type),
                                                machine_image=linux_ami,
                                                role=iam.Role.from_role_arn(self,
                                                                            "Role",
                                                                            prd_role,
                                                                            mutable=False
                                                                           ),
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                               )

        self.asg.connections.allow_from(alb,ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        core.CfnOutput(self, "Output",
                       value=alb.load_balancer_dns_name)

class devEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        alb = elb.ApplicationLoadBalancer(self, "AppLB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="AppLB"
                                         )
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        listener=alb.add_listener("port80",
                                  port=80,
                                  open=True)

        self.asg = autoscaling.AutoScalingGroup(self, "ASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=dev_ec2_type),
                                                machine_image=linux_ami,
                                                role=iam.Role.from_role_arn(self,
                                                                            "Role",
                                                                            dev_role,
                                                                            mutable=False
                                                                           ),
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                               )


        worker_utilization_metric = cloudwatch.Metric(
                        namespace="MyService",
                        metric_name="WorkerUtilization"
        )

        self.asg.scale_on_metric("ScaleToCPU",
                 metric=worker_utilization_metric,
                 scaling_steps=[
                     {"upper": 10, "change": -1},
                     {"lower": 50, "change": +1},
                     {"lower": 70, "change": +3}
                 ],
                 adjustment_type=autoscaling.AdjustmentType.PERCENT_CHANGE_IN_CAPACITY
                )


        self.asg.connections.allow_from(alb,ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        core.CfnOutput(self, "Output",
                       value=alb.load_balancer_dns_name)
