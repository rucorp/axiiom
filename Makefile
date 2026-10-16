SHELL := /bin/sh
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all generate test build clean generate-mock-services-seo

all: generate test

generate: generate-docs generate-demos generate-industries generate-mock-services-seo generate-sitemap

generate-docs:
	cd $(ROOT)docs && python3 generate_docs.py

generate-demos:
	cd $(ROOT)demo/app && python3 generate_demos.py

generate-industries:
	cd $(ROOT) && python3 generate_industries.py
	cd $(ROOT) && python3 generate_industries_index.py

generate-mock-services-seo:
	python3 $(ROOT)patch_mock_services_seo.py

generate-sitemap:
	cd $(ROOT) && python3 generate_sitemap.py

test:
	python3 $(ROOT)test_seo.py
	python3 $(ROOT)test_site.py --exit-code

test-serve:
	python3 $(ROOT)test_site.py --serve --exit-code

build:
	docker build -t axiiom-site $(ROOT)

clean:
	rm -f $(ROOT)test-report.html
