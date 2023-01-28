cleanup:
	poetry run black aws_cdk_infrastructure/
	poetry run black app.py

deploy:
	cdk deploy --all

diff:
	cdk diff