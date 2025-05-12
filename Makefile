.PHONY: debug test \
	fixtures


#
# NOTES
# - that the "-n1" flag captures all output
# - "-x" halt on first fail

# vars
DATE := $(shell date +%Y-%m-%d)
REPORT_DIR := reports
REPORT_FILE := $(REPORT_DIR)/$(DATE).md

install:
	pip install -r requirements.txt && playwright install chromium

debug:
	clear \
	; pytest -s test_ocean_metrics.py

test:
	clear \
	&& rm -f "$(REPORT_DIR)/*.md" \
	; pytest -vs \
	; tree "$(REPORT_DIR)" \
	; cat "$(REPORT_FILE)" \
	; echo "ok"


# test-serial:
# 	pytest -vs -n1 -m 'serial'
#
# test-parallel:
# 	pytest -vs -m 'not serial'

watch:
	ls *.py | entr make test

# watch-serial:
# 	ls *.py | entr make serial
#
# watch-parallel:
# 	ls *.py | entr make parallel
