SHELL := /bin/sh
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all generate test build clean

all: generate test

generate: generate-docs generate-demos generate-industries generate-sitemap

generate-docs:
	cd $(ROOT)docs && python3 generate_docs.py

generate-demos:
	cd $(ROOT)demo/app && python3 generate_demos.py

generate-industries:
	cd $(ROOT) && python3 generate_industries.py

generate-sitemap:
	cd $(ROOT) && python3 generate_sitemap.py

test:
	python3 $(ROOT)test_site.py --exit-code

test-serve:
	python3 $(ROOT)test_site.py --serve --exit-code

build:
	docker build -t axiiom-site $(ROOT)

clean:
	rm -f $(ROOT)test-report.html
