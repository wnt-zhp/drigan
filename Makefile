
docs:
	export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"; cd docs; make html


.PHONY: docs
