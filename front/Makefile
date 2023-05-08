run:
	pipenv run streamlit run app.py

build:
	docker build --platform linux/amd64 -t 219494815276.dkr.ecr.ap-northeast-1.amazonaws.com/kok-hashimoto-improved-fishstick:latest .

push:
	docker push 219494815276.dkr.ecr.ap-northeast-1.amazonaws.com/kok-hashimoto-improved-fishstick:latest

deploy:
	aws apprunner create-service --cli-input-json file://app-runner.json
