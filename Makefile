deploy-github-page:
	git clone https://github.com/FinMind/FinMind.git ../finmind-github && \
	rm -r -f ../finmind-github/* && \
	mv * ../finmind-github/ && \
	cp .travis.yml ../finmind-github/ && \
	cd ../finmind-github/ && \
	git config user.name "sam" && git config user.email "finmind.tw@gmail.com" && \
	git remote set-url origin https://gitlabci:${GITHUB_TOKEN}@github.com/FinMind/FinMind.git && \
	git add . && git commit -m "${CI_COMMIT_TITLE}" && git tag ${CI_COMMIT_TAG} && \
	git push origin master && git push origin ${CI_COMMIT_TAG}


install-python-evn:
	sudo apt-get update && \
	sudo apt-get install python3-pip -y && \
	pip3 install setuptools && \
	pip3 install twine

build-dist:
	CI_COMMIT_TAG=${CI_COMMIT_TAG} python3 setup.py sdist

upload-pypi:
	twine upload -u ${TWINE_USERNAME} -p ${TWINE_PASSWORD} dist/*

req:
	pipenv lock --requirements > requirements.txt

linux-wheel:
	pip wheel ./ -w wheelhouse/

format:
	black -l 80 FinMind tests

