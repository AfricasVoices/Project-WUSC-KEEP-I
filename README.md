# Project-WUSC-KEEP-II

This repository contains Dockerised data pipeline stages for the WUSC-KEEP-II project, and a collection of Bash scripts
for executing both those stages and the SMS platform data fetcher over WUSC-KEEP data.

## Usage
### Prerequisites
#### Tools
Install Python 3.7, Pipenv, and Docker.

#### SMS Fetcher
The data fetching stages of the pipeline require access to a local copy of the 
[Echo Mobile fetcher](https://github.com/AfricasVoices/EchoMobileTools) project.
To configure this:
 
1. Clone that repository to your local system:

   `$ git clone https://github.com/AfricasVoices/EchoMobileTools.git`


1. Checkout the appropriate commit for this project:

   `$ git checkout 423fecc4325b5f5d6852699cb4608bb7dd5cf446`  # TODO: Tag EchoMobileExperiments appropriately

1. Install project dependencies:
   ```bash
   $ cd EchoMobileExperiments
   $ pipenv --three
   $ pipenv sync
   ```

1. When using the fetch scripts in `run_scripts/`, set the `<echo-mobile-root>` argument to the absolute path 
   to the directory just cloned. For example:

   `$ sh 01_fetch_messages.sh test_user /Users/test_user/EchoMobileExperiments ...`
