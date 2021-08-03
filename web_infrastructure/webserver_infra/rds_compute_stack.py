import os
from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class prdRdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc,
                 asg_security_groups,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db_mysql = rds.DatabaseInstance(self, "RDS-MySQL",
                                        engine=rds.DatabaseInstanceEngine.mysql(
                                            version=rds.MysqlEngineVersion.VER_5_7_30

                                        ),
                                        instance_type=ec2.InstanceType.of(
                                            ec2.InstanceClass.BURSTABLE2,
                                            ec2.InstanceSize.LARGE),
                                        vpc=vpc,
                                        multi_az=True,
                                        allocated_storage=100,
                                        storage_type=rds.StorageType.GP2,
                                        cloudwatch_logs_exports=["audit",
                                                                 "error",
                                                                 "general",
                                                                 "slowquery"],
                                        deletion_protection=False,
                                        backup_retention=core.Duration.days(7),
                                       )

        for asg_sg in asg_security_groups:
            db_mysql.connections.allow_default_port_from(asg_sg, "EC2 \
                                                         Autoscaling Group \
                                                         access MySQL")

class devRdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc,
                 asg_security_groups,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db_mysql = rds.DatabaseInstance(self, "RDS-MySQL",
                                        engine=rds.DatabaseInstanceEngine.mysql(
                                            version=rds.MysqlEngineVersion.VER_5_7_30

                                        ),
                                        instance_type=ec2.InstanceType.of(
                                            ec2.InstanceClass.BURSTABLE2,
                                            ec2.InstanceSize.SMALL),
                                        vpc=vpc,
                                        multi_az=False,
                                        allocated_storage=100,
                                        storage_type=rds.StorageType.GP2,
                                        cloudwatch_logs_exports=["audit",
                                                                 "error",
                                                                 "general",
                                                                 "slowquery"],
                                        deletion_protection=False,
                                        backup_retention=core.Duration.days(7),
                                       )


        for asg_sg in asg_security_groups:
            db_mysql.connections.allow_default_port_from(asg_sg, "EC2 \
                                                         Autoscaling Group \
                                                         access MySQL")

