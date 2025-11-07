FROM public.ecr.aws/lambda/python:3.13

COPY src ${LAMBDA_TASK_ROOT}
COPY pyproject.toml ${LAMBDA_TASK_ROOT}

RUN pip install ${LAMBDA_TASK_ROOT}

# NOTE: handler set as CMD by  parameter override outside of the Dockerfile
# CMD [ "lambda_function.handler" ]
