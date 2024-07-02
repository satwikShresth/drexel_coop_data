BUN=bun
SRC=app

all: setup run

setup: ${SRC}
	cd ${SRC} && $(BUN) install

run: ${SRC}
	cd ${SRC} && $(BUN) run dev

resetup: clean setup
