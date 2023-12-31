MYNAME = EldarKasmamytov
PACKAGE = MiniC
# Example: stop at the first failed test:
#   make PYTEST_OPTS=-x tests
PYTEST_OPTS = 
# Run the whole test infrastructure for a subset of test files e.g.
#   make TEST_FILES='TP03/**/bad*.c' tests
ifdef TEST_FILES
export TEST_FILES
endif

ifdef SSA
export ENABLE_SSA=1
endif

PYTEST_BASE_OPTS=-vv -rs --failed-first --cov="$(PWD)" --cov-report=term --cov-report=html

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif

all: antlr

.PHONY: antlr
antlr MiniCLexer.py MiniCParser.py: $(PACKAGE).g4
	$(ANTLR4) $< -Dlanguage=Python3 -visitor -no-listener

main-deps: MiniCLexer.py MiniCParser.py TP03/MiniCInterpretVisitor.py TP03/MiniCTypingVisitor.py

.PHONY: tests tests-interpret tests-codegen clean clean-tests tar antlr


tests: tests-interpret tests-codegen

tests-pyright: antlr
	pyright .

tests-interpret: tests-pyright test_interpreter.py main-deps
	python3 -m pytest $(PYTEST_BASE_OPTS) $(PYTEST_OPTS) test_interpreter.py


# Test for naive allocator (also runs test_expect to check // EXPECTED directives):
tests-naive: tests-pyright antlr
	python3 -m pytest $(PYTEST_BASE_OPTS) $(PYTEST_OPTS) ./test_codegen.py -k 'naive or expect'

# Test for all but the smart allocator, i.e. everything that lab4 should pass:
tests-notsmart: tests-pyright antlr
	python3 -m pytest $(PYTEST_BASE_OPTS) $(PYTEST_OPTS) ./test_codegen.py -k 'not smart'

# Test just the smart allocation (quicker than tests)
tests-smart: tests-pyright antlr
	python3 -m pytest $(PYTEST_BASE_OPTS) $(PYTEST_OPTS) ./test_codegen.py -k 'smart'

# Complete testsuite (should pass for lab5):
tests-codegen: tests-pyright antlr
	python3 -m pytest $(PYTEST_BASE_OPTS) $(PYTEST_OPTS) ./test_codegen.py

tests-optim: tests-pyright antlr
	ENABLE_SSA=1 SSA_OPTIMS=1 python3 -m pytest $(PYTEST_BASE_OPTS) $(PYTEST_OPTS) ./test_codegen.py

tar: clean
	dir=$$(basename "$$PWD") && cd .. && \
	tar cvfz $(MYNAME).tgz --exclude="*.riscv" --exclude=".git" --exclude=".pytest_cache"  \
	--exclude="htmlcov" "$$dir"
	@echo "Created ../$(MYNAME).tgz"

# Remove any assembly file that was created by a test.
# Don't just find -name \*.s -exec rm {} \; because there may be legitimate .s files in the testsuite.
define CLEAN
import glob
import os
for f in glob.glob("**/tests/**/*.c", recursive=True):
	for s in ("{}-{}.s".format(f[:-2], test) for test in ("naive", "smart", "gcc", "all_in_mem")):
		try:
			os.remove(s)
			print("Removed {}".format(s))
		except OSError:
			pass
endef
export CLEAN
clean-tests:
	@python3 -c "$$CLEAN"

clean: clean-tests
	find . \( -iname "*~" -or -iname ".cache*" -or -iname "*.diff" -or -iname "log*.txt" -or -iname "__pycache__" -or -iname "*.tokens" -or -iname "*.interp" \) -print0 | xargs -0 rm -rf \;
	rm -rf *~ $(PACKAGE)Parser.py $(PACKAGE)Lexer.py $(PACKAGE)Visitor.py .coverage .benchmarks
