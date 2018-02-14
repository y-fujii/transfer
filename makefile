.PHONY: all
all: build/transfer build/transfer.pdf

build/transfer: src/transfer.cpp
	mkdir -p build
	$(CXX) -std=gnu++14 -pedantic -Wall -Wextra -O3 -o build/transfer src/transfer.cpp -isystem /usr/include/eigen3

build/transfer.pdf: doc/transfer.tex build/plot.pdf
	mkdir -p build
	cd build && lualatex --halt-on-error ../doc/transfer.tex && lualatex --halt-on-error ../doc/transfer.tex

build/data.txt: build/transfer
	build/transfer | tee build/data.txt
