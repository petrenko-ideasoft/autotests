# HAQQ


### Tools
* Python
* Behave
* Report Portal
* Requests
* PyCharm Pro (Optional)

### Env variables
| Variable name            | Description                                                                    | Type     |
|--------------------------|--------------------------------------------------------------------------------|----------|
| BASE_URL                 | Which URL to use in tests. http://localhost:8481/backend is default            | `string` |
| ACCOUNT_ADDRESS          | Wallet address                                                                 | `string` |

### Config variables
If no need to run on different servers, there is a possibility to specify constantly next next
base_url: base url
account_address: wallet address
private_key: private key of wallet
chain_id: chain id of network

Important: for execute emails tests wallet from which they will be executed must be granted

### Test Execution
This project has been grouped and organized by type, feature and functionality, in order to complete a test execution you have two options
1. Thru PyCharm
    * Go to the desired feature file under `/features`
    * For the scenario Click on the two green arrows for the desired scenario
    * Click on `Run ...`
    
2. Thru console/terminal
    * Access project's folder
    * execute `behave --tags=@[TEST_SUITE_FROM_FEATURE_FILE]` [^1]
    
3. Add Behave config for Report portal
    
    * Create behave.local.ini file and add following data. 
    * rp_token can be found on Report Portal -> User profile 
    * rp_project = personal project page
    * rp_launch_name = Description of the launch name

### Parallel test executions
The implementation for running tests in parallel is based on concurrent Behave instances executed in multiple processes.

As part of the wrapper constraints, this approach implies that whatever you have in the Python Behave hooks in environment.py module, it will be re-executed on every parallel process.

BehaveX will be in charge of managing each parallel process, and consolidate all the information into the execution reports

Parallel test executions can be performed by feature or by scenario.

Examples:

`behavex -t @<TAG> --parallel-processes 2 --parallel-schema scenario`

`behavex -t @<TAG> --parallel-processes 5 --parallel-schema feature`

When the parallel-schema is set by feature, all tests within each feature will be run sequentially.

After parallel execution report will be generated in `/output` folder


### Report portal
````
    rp_endpoint = http://domain.name/
    rp_project = project_name
    rp_token = xxxxxxxx-xxxx-xxxx-xxxx-d8eafb811f15
    rp_launch_name = 'Debug mode'
    rp_launch_description = ''
````

### Project Structure
**app** - contains declared pages of application

**config** - configuration files for global and local usage. There are data like base url, users, roles or other data which should be populated

**features** - folders with feature files where there scenarios and step definitions for them
-   **steps** - folder for files which has the step implementation organized by page/feature

**helpers** - python files which may help with tests data manipulating. Such as API client, data generator etc.

**reports** - xml extension file for execution from terminal

**schemas** - described response structure

**requests_data** - json predefined data which may be used in requests


#### Important Files Information
Certain files are important to know what relevant information they hold when you want to first start creating test cases and/or setting up the framework locally.
- `config.yml` and `config.local.yml` has data and framework information, when `Behave` starts test run, one of the first file that are called is `config.local.yml` if it exits, else it will take data from `config.yml` that's generally used for `CI/CD` environments, you may check that on `helpers/configurator.py` file. So in this file you'll need to place your information to login.
- `features/environment.py` holds configuration before tests gets executed, report portal all everything needed before steps are executed. 

### Gherkin
Gherkin is plain text where test cases are specified in common language as english, (e.g. `wallets.feature`) and it's linked to test scripts to be executed, you can refer to this [link](https://cucumber.io/docs/gherkin/ "Gherkin") for more information, but to mention one of many benefits, it's a common place were different organization roles can converge to verify what's being tested / covered, one other benefit of using such tool, is that this allows test re-utilization, as there can be another test case inside the test case suite that requires the same step, please also check this example for further visualization

### Reporting
Report portal is online reporting system where we can see tests results execution in real time and do not need for hours to get current state on tests. If fail occurred, we can see it and start investigation of it when other tests are in execution progress.
<br>
Report files are stored under `/reports` as `XML`.
**TBC with images**