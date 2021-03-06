# python-traceview

The 'oboe' and 'oboeware' modules provide support for instrumenting
programs for use with the TraceView Oboe instrumentation library.

The oboe module provides a Pythonic interface to liboboe for C, and
the oboeware module provides middleware and other components for
popular web frameworks such as Django, Tornado, Pylons, and WSGI.

## Installing

The Python instrumentation for TraceView uses a module named `oboe`, which you
can get from pip by running:

```sh
pip install oboe
```

NOTE: Make sure you've first done the [base TraceView install](http://docs.traceview.solarwinds.com/TraceView/install-instrumentation.html) so the appropriate dependencies are available.

## Configuring

See our documentation on [configuring TraceView for python](http://docs.traceview.solarwinds.com/Instrumentation/python.html#configuring-instrumentation).

# Upgrading

To upgrade an existing installation, you simply need to run:

```sh
pip install oboe --upgrade
```

## Running the Tests

### Test dependencies

The test suite depends on the presence of several database and cache servers.

- mysql
- postgres
- mongodb
- memcached
- redis

The test suite uses [tox](https://testrun.org/tox/latest/), a tool for running
tests against different versions of python and depended modules. You can get it
from apt by running `sudo apt-get install python-tox` or from pip with
`sudo pip install tox`.

The tests currently run against python 2.6 and 2.7, so you will need both.

To set up multiple versions of python:

    sudo apt-get install python-software-properties software-properties-common
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python2.6 python2.6-dev

### Configuring test database and cache servers

MySQL SQLAlchemy tests require no-auth TCP connection (as testing user).

PostgreSQL SQLAlchemy tests requires no-auth (trust) TCP connection (as testing user).

```
# in pg_hba.conf: Don't use this in production!!
host    all             all             127.0.0.1/32            trust
```

### Running the tests

To run tests, simply run:

```sh
tox
```

### Test directory layout

Tests in test/unit are actually functional tests; naming is for historic
reasons.  Tests in test/manual are for manual verification of certain
behaviors.

## Support

If you find a bug or would like to request an enhancement, feel free to file
an issue. For all other support requests, see our [support portal](tracelytics.freshdesk.com).

## Contributing

You are obviously a person of great sense and intelligence. We happily
appreciate all contributions to the oboe module whether it is documentation,
a bug fix, new instrumentation for a library or framework or anything else
we haven't thought of.

We welcome you to send us PRs. We also humbly request that any new
instrumentation submissions have corresponding tests that accompany
them. This way we don't break any of your additions when we (and others)
make changes after the fact.

## Developer Resources

We have made a large effort to expose as much technical information
as possible to assist developers wishing to contribute to the traceview module.
Below are the three major sources for information and help for developers:

* The [TraceView Knowledge Base](http://docs.traceview.solarwinds.com/)
has a large collection of technical articles or, if needed, you can submit a
support request directly to the team.

If you have any questions or ideas, don't hesitate to contact us anytime.

## Compiling the C extension

This module utilizes a C++ extension to interface with the system `liboboe.so`
library.  This system library is installed with the TraceView host packages
(tracelyzer, liboboe0, liboboe-dev) and is used to report
host and performance metrics
from multiple sources (nodejs, nginx, python etc.) back to TraceView servers.

Note: Make sure you have the development package `liboboe0-dev` installed
before attempting to compile the C extension.

```bash
>$ dpkg -l | grep liboboe
ii  liboboe-dev  1.2.1-trusty1  TraceView common library -- development files
ii  liboboe0     1.2.1-trusty1  Traceview common library
```

See [Installing Base Packages on Debian and Ubuntu](http://docs.traceview.solarwinds.com/TraceView/install-instrumentation.html#debian-and-ubuntu)
in the Knowledge Base for details.

To see the code related to the C++ extension, take a look in `oboe`.

## License

Copyright (c) 2016 SolarWinds, LLC

Released under the [Librato Open License](http://docs.traceview.solarwinds.com/Instrumentation/librato-open-license.html)
