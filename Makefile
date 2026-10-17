.PHONY: install run test dashboard

install:
	pip install -e ".[dashboard,llm,dev]"

run:
	python scripts/run_pipeline.py --config config/default.yaml

test:
	pytest -q

dashboard:
	streamlit run dashboard/app.py
