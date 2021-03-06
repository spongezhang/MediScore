#!/bin/bash

source detection_tests.sh

echo
echo "CASE 1: VALIDATING FULL SCORING WITH BASELINEs"
echo
run_test test_c1_1 "$testsuite_directory/checkfiles/test_c1_1"
run_test test_c1_2 "$testsuite_directory/checkfiles/test_c1_2"
run_test test_c1_3 "$testsuite_directory/checkfiles/test_c1_3"

echo
echo "CASE 2.1: VALIDATING SYSTEM OUTPUT TESTCASEs"
echo
run_test test_c2_1 "$testsuite_directory/checkfiles/test_c2_1"
run_test test_c2_2 "$testsuite_directory/checkfiles/test_c2_2"
run_test test_c2_3 "$testsuite_directory/checkfiles/test_c2_3"
run_test test_c2_4 "$testsuite_directory/checkfiles/test_c2_4"
run_test test_c2_5 "$testsuite_directory/checkfiles/test_c2_5"

echo
echo "CASE 2.2: VALIDATING SYSTEM OUTPUT TESTCASEs with the OptOut option"
echo
run_test test_c2_6 "$testsuite_directory/checkfiles/test_c2_6"
run_test test_c2_7 "$testsuite_directory/checkfiles/test_c2_7"
run_test test_c2_8 "$testsuite_directory/checkfiles/test_c2_8"
run_test test_c2_9 "$testsuite_directory/checkfiles/test_c2_9"


echo
echo "CASE 3: VALIDATING FULL INDEX and SUBSET INDEX FILEs"
echo
run_test test_c3_1 "$testsuite_directory/checkfiles/test_c3_1"
run_test test_c3_2 "$testsuite_directory/checkfiles/test_c3_2"
run_test test_c3_3 "$testsuite_directory/checkfiles/test_c3_3"
run_test test_c3_4 "$testsuite_directory/checkfiles/test_c3_4"


echo
echo "CASE 4: VALIDATING QUERIES WITH JOURNALING MASK JOIN"
echo
run_test test_c4_1 "$testsuite_directory/checkfiles/test_c4_1"
run_test test_c4_2 "$testsuite_directory/checkfiles/test_c4_2"
run_test test_c4_3 "$testsuite_directory/checkfiles/test_c4_3"


echo
echo "CASE 5: VALIDATING ALL THE EXAMPLES FROM THE DETECTIONSCORER README DOCUMENT"
echo
run_test test_c5_1 "$testsuite_directory/checkfiles/test_c5_1"
