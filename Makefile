run-app-poetry:
	poetry run streamlit run streamlit_app.py

run-app:
	streamlit run streamlit_app.py

clean-code:
	poetry run black .