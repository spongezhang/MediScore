#!/bin/bash

export testsuite_directory=../../data/test_suite/mytest_MSCOCO_synthesized

python ./ProvenanceFilteringScorer.py -o "$testsuite_directory/checkfiles/mytest" \
			   -x "$testsuite_directory/MSCOCO_synthesized-provenancefiltering-index.csv" \
			   -r "$testsuite_directory/MSCOCO_synthesized-provenancefiltering-ref.csv" \
			   -n "$testsuite_directory/MSCOCO_synthesized-provenancefiltering-ref-node.csv" \
			   -w "$testsuite_directory/MSCOCO_synthesized-provenancefiltering-world.csv" \
			   -R "$testsuite_directory/" \
			   -s "$testsuite_directory/output.csv" \
			   -S "$testsuite_directory/"
