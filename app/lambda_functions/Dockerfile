FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY app.py ${LAMBDA_TASK_ROOT}

CMD ["app.lambda_handler"]