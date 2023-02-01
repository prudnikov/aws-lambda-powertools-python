import requests

from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.typing import LambdaContext


def lambda_handler(event: dict, context: LambdaContext):
    try:
        # Retrieve multiple parameters from a path prefix
        all_parameters: dict = parameters.get_parameters("/lambda-powertools/", max_age=20)
        endpoint_comments = None

        for parameter, value in all_parameters.items():

            if parameter == "endpoint_comments":
                endpoint_comments = value

        if endpoint_comments is None:
            return {"comments": None}

        # the value of parameter is https://jsonplaceholder.typicode.com/comments/
        comments: requests.Response = requests.get(endpoint_comments)

        return {"comments": comments.json()[:10]}
    except parameters.exceptions.GetParameterError as error:
        return {"comments": None, "message": str(error), "statusCode": 400}
