.PHONY: all
all: build/transfer build/transfer.pdf

build/transfer: src/transfer.cpp
	mkdir -p build
	$(CXX) -std=gnu++14 -pedantic -Wall -Wextra -O3 -o build/transfer src/transfer.cpp -isystem /usr/include/eigen3

build/transfer.pdf: src/plot.py doc/transfer.tex
	python3 src/plot.py
	mkdir -p build
	cd build && lualatex --halt-on-error ../doc/transfer.tex && lualatex --halt-on-error ../doc/transfer.tex
	cp build/transfer.pdf /var/www/html/

build/data.txt: build/transfer
	build/transfer | tee build/data.txt
