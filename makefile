.PHONY: all
all: build/transfer build/transfer.pdf

build/transfer: src/transfer.cpp
	mkdir -p build
	$(CXX) -std=gnu++14 -pedantic -Wall -Wextra -O3 -o build/transfer src/transfer.cpp -isystem /usr/include/eigen3

build/transfer.pdf: doc/transfer.tex
	mkdir -p build
	cd build && lualatex --halt-on-error ../doc/transfer.tex && lualatex --halt-on-error ../doc/transfer.tex

.PHONY: run
run: build/transfer
	build/transfer | tee build/data.txt

.PHONY: clean
clean:
	rm -rf build
