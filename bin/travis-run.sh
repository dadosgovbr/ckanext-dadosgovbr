#!/bin/sh -e

# Test: Check build
# ===========================================================
nosetests --ckan --nologcapture --with-pylons=subdir/test.ini ckanext/dadosgovbr

# Test: Front-end
# ===========================================================

# Start CKAN server
cd ckan
paster serve test-core.ini &
cd -
sleep 5 # Make sure the server has fully started

# Run test
mocha-phantomjs http://localhost:5000/base/test/index.html

# Did an error occur?
MOCHA_ERROR=$?

# We are done so kill CKAN
killall paster

# Test: All nosetests
# ===========================================================
nosetests --ckan --reset-db --with-pylons=subdir/test.ini --nologcapture --with-coverage --cover-package=ckan --cover-package=ckanext ckanext/dadosgovbr

# Did an error occur?
NOSE_ERROR=$?
[ "0" -ne "$MOCHA_ERROR" ] && echo MOCHA tests have failed
[ "0" -ne "$NOSE_ERROR" ] && echo NOSE tests have failed


# Error output to Travis
# ===========================================================
exit `expr $MOCHA_ERROR + $NOSE_ERROR`
