PY=python
FA=fastapi
VE=venv
REQ=requirement.txt
SRC=app

all: setup

setup: ${REQ} ${SRC}
	${PY} -m ${VE} .${VE}
	./.${VE}/bin/pip install -r ${REQ}

run: ${SRC}
	./.${VE}/bin/${FA} dev ${SRC}

clean:
	rm -rf .${VE}

resetup: clean setup
