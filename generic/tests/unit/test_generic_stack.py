import aws_cdk as core
import aws_cdk.assertions as assertions

from generic.generic_stack import GenericStack

# example tests. To run these tests, uncomment this file along with the example
# resource in generic/generic_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GenericStack(app, "generic")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
