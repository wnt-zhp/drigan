
docs:
	export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"; cd docs; make html

styles:
	lessc -x --clean-css drigan/static/less/style.less drigan/static/style.css


.PHONY: docs
