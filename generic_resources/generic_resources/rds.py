from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    # aws_sqs as sqs,
)
import aws_cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
from constructs import Construct


class rdsMysql(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, asg_security_groups, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        db_mysql = rds.DatabaseInstance(self, "RDS-MySQL",
                                        engine=rds.DatabaseInstanceEngine.mysql(
                                            version=rds.MysqlEngineVersion.VER_5_7_30

                                        ),
                                        instance_type=ec2.InstanceType.of(
                                            ec2.InstanceClass.BURSTABLE2,
                                            ec2.InstanceSize.SMALL),
                                        vpc=vpc,
                                        multi_az=True,
                                        allocated_storage=100,
                                        storage_type=rds.StorageType.GP2,
                                        cloudwatch_logs_exports=["audit",
                                                                 "error",
                                                                 "general",
                                                                 "slowquery"],
                                        deletion_protection=False,
                                        backup_retention=aws_cdk.Duration.days(7),
                                        )

        for asg_sg in asg_security_groups:
            db_mysql.connections.allow_default_port_from(asg_sg, "EC2 \
                                                         Autoscaling Group \
                                                         access MySQL")
