import aws_cdk as core
import aws_cdk.assertions as assertions

from generic_resources.generic_resources_stack import GenericResourcesStack

# example tests. To run these tests, uncomment this file along with the example
# resource in generic_resources/generic_resources_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GenericResourcesStack(app, "generic-resources")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
