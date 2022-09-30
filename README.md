![Custom badge](https://img.shields.io/endpoint?color=%23&style=flat-square&url=https%3A%2F%2Fsplunkbasebadge.livehybrid.com%2Fv1%2Fdownloads%2F2734)
![contributors-shield](https://img.shields.io/github/contributors/splunk/utbox.svg?style=flat-square)

<div align="center">
<h3 align="center">URL Toolbox</h3>

  <p align="center">
    Building blocks for URL Manipulation in Splunk Enterprise
    <br />
    <br />
    <a href="https://github.com/splunk/utbox/blob/master/utbox/appserver/static/documentation.pdf">Documentation</a>
    ·
    <a href="https://github.com/splunk/utbox/issues">Report Bug</a>
    ·
    <a href="https://splunkbase.splunk.com/app/2734/">Splunkbase</a>
  </p>
</div>

## About The Project

URL Toolbox (UTBox) is a set of building blocks for Splunk specially created for URL manipulation. UTBox has been created to be modular, easy to use and easy to deploy in any Splunk environments. 

One of the core feature of UTBox is to correctly parse URLs and complicated TLDs (Top Level Domain) using the Mozilla Suffix List. Other functions like shannon entropy, counting, suites, meaning ratio, bayesian analysis, etc, are also available.

UTBox has firstly be created for security analysts but may fit other needs as it’s a set of building blocks. UTBox only needs to be deployed on Splunk Search Heads (the bundles will automatically be sent to your Splunk Indexers). Finally, each lookups is shipped with a macro to make it easier to use.

[Read about this app on Splunk Blogs!](https://www.splunk.com/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html)

## Getting Started

This section outlines the steps required to use the app on a Splunk Enterprise environment. If you want to develop the code base further, refer to the [Development](##development) section of this README.


### Prerequisites

- **Splunk Enterprise / Cloud**: Refer to [Splunkbase](https://splunkbase.splunk.com/app/2734/) for supported versions.

### Installation

The easiest way to install the URL Toolbox is via the in-product app browser (Manage Apps -> Browse More Apps). It will allow you to install the latest version from [Splunkbase](https://splunkbase.splunk.com/app/2734/).

If you need a specific version of the app or you want to inspect the app bundle before installation, please refer to the [Splunk Documentation](https://docs.splunk.com/Documentation/AddOns/released/Overview/Installingadd-ons) for your respective platform.
This app needs to be installed on the Search tier of your deployment. 

## Usage

This app provides a set of macros that simplify the interaction with the bundled lookups.

Please find below some selected samples of commands and their respective output. Please find more in-depth examples and explanation [in the docs](utbox/appserver/static/documentation.pdf).


### ut_parse_simple

**SPL**
```
|makeresults count=1 
| eval url="https://splunk.com" 
| `ut_parse_simple(url)`
```

**Output**
|_time                       |url               |ut_fragment|ut_netloc |ut_params|ut_path|ut_query|ut_scheme|
|----------------------------|------------------|-----------|----------|---------|-------|--------|---------|
|2021-12-16T10:29:07.000+0000|https://www.splunk.com/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html|None       |www.splunk.com|None     |/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html|None    |https    |

## ut_parse

**SPL**
```
|makeresults count=1 
| eval url="https://www.splunk.com/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html", list="*" 
| `ut_parse(url, list)`
```
**Output**
|_time                       |list              |url |ut_domain |ut_domain_without_tld|ut_fragment|ut_netloc|ut_params|ut_path                                                          |ut_port|ut_query|ut_scheme|ut_subdomain|ut_subdomain_count|ut_subdomain_level_1|ut_tld|
|----------------------------|------------------|----|----------|---------------------|-----------|---------|---------|-----------------------------------------------------------------|-------|--------|---------|------------|------------------|--------------------|------|
|2021-12-16T10:30:00.000+0000|*                 |https://www.splunk.com/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html|splunk.com|splunk               |None       |www.splunk.com|None     |/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html|80     |None    |https    |www         |1                 |www                 |com   |

## ut_shannon

**SPL**
```
|makeresults count=1 
| eval url="buttercup" 
| `ut_shannon(url)`
```

**Output**
|_time                       |url               |ut_shannon|
|----------------------------|------------------|----------|
|2021-12-16T10:32:19.000+0000|buttercup         |2.725480556997868|

## ut_countset

**SPL**
```
|makeresults count=1 
| eval url="buttercup"
| eval set="tu" 
| `ut_countset(url,set)`
```

**Output**
|_time                       |set               |url |ut_countset                                  |
|----------------------------|------------------|----|---------------------------------------------|
|2021-12-16T10:34:17.000+0000|tu                |buttercup|{"ut_countset": {"sum": 4, "74": 2, "75": 2}}|


## Development

### Development Setup

1. Clone this repository
2. Symlink the `utbox` directory to your `$SPLUNK_HOME/etc/apps/` directory.

### Creating a release bundle

Run the `package` target in the provided Makefile.
```
make package
```


## License

Please refer to the [License on Splunkbase.](https://cdn.apps.splunk.com/static/misc/eula.html)

## Bug Fixes / Enhancement Requests

🐞 ✍🏼 💡 Create [issue](https://github.com/splunk/utbox/issues/new) with appropriate label to submit the request.

## Troubleshooting

**SPL**: `index=_internal ERROR *bin/ut_*py`


## Acknowledgments

* Cedric Le Roux
* [Ian Forrest](https://github.com/iforrest)
* [Daniel Federschmidt](https://github.com/dfederschmidt)
