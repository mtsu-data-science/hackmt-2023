run-app-poetry:
	poetry run streamlit run streamlit_app.py

run-app:
	streamlit run streamlit_app.py

clean-code:
	poetry run black .

setup-requirements-file:
	poetry export -f requirements.txt --output requirements.txt

setup-dev-requirements-file:
	poetry export --dev -f requirements.txt --output anaconda-environment.txt

setup-requirements:
	poetry export -f requirements.txt --without-hashes --output requirements.txt

setup-conda:
	poetry export --dev -f requirements.txt --without-hashes --output anaconda-environment.txt