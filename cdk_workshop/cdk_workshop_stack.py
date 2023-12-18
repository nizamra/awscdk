from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter

class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # queue = sqs.Queue(
        #     self, "CdkWorkshopQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        # topic = sns.Topic(
        #     self, "CdkWorkshopTopic"
        # )
        # topic.add_subscription(subs.SqsSubscription(queue))

        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter.handler,
        )
        TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
            sort_by="-hits"
        )