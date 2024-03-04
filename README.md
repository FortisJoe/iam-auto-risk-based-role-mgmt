
# Identity &amp; Access Management System: Automated Risk-Based Role Management Approach

The code in this project is components developed for the Bravura Security Identity system to provide automated role management in a risk managed approach - specifically to handle deviations of access from a users defined roles.

The aim of this project is to develop a methodology to assess the risk of under and over provisioned access based on a role based access system within an Identity and Access Management system, and to develop software to integrate with the Bravura Identity system, based on the developed methodology to calculate risk of under and over provisioned access and act based on predefined thresholds.

## Installation

The components require an existing Bravua Security Identity system to be installed - see the installation instructions on the [Bravura Security Documentation Website.](https://bravurasecuritydocs.com/#/home/Installing_the_Bravura_Security_Fabric_server_software/10/11)

Download the source code and merge the files into the root folder of the instance.

Before installation of the components, edit the classification data, and mako templates for emails to meet your needs.

Open the Bravura Security Fabric Command Prompt as an Administrator, changing directory to the script folder and running the following commands:

`manage_components.py load`

`manage_components.py install Scenario.role_deviation_risk_management`

## Configuration

Each managed group and template should have the surplus (user has entitlement without a role definition to match it) and deficit (user should have entitlment according to the role definitions, but does not have it) risk scores defined, as well as how often a risk should be exploited or how much it would cause issues with availability, in terms of a rate of occurance - this is times per year.

![Configuration](https://i.ibb.co/MsP0fhc/screenshot.png)

The risk levels should be configured to match your risk acceptance levels, in the extdb table role_deviation_risk_classification_evaluation_treatment

![Table](https://i.ibb.co/LZS2pdd/Capture-Table.png)

## Usage

There are 3 mechanisms in how this system will undertake automated risk-based role management.

### Upon Request Completion

Upon Request Completion, the recipient of the request will have the access they do have, compared to the access they should have according to the role definitions of the roles they are members of. Any surplus or deficit is sent for analysis.

### Upon detected changes from targetted systems

After a discovery takes place, changes on target systems for each user will be detected for accounts and group memberships of a target system by idtrack. For each of these changes, the changed access will be compared to the access they should have according to the role definitions of the roles they are members of. Any surplus or deficit is sent for analysis.

### Periodic Checks

Periodically, for all users, each user will have the access they do have, compared to the access they should have according to the role definitions of the roles they are members of. Any surplus or deficit is sent for analysis.

### Analysis

The risk score is calculated according to the following algorithm

Let us make the following definitions:

	a - The availability impact, from 0 to 10.

	c - The confidentiality impact, from 0 to 10.

	i - The integrity impact, from 0 to 10.
 
	aro - The annual rate of occurrence.    

	r - The calculated risk level. 

We can then define our risk calculation as the following:

r=aro×(a+c+i)

The calculated risk score is then sent for Evaluation

### Evaluation

The risk score is compared to the various treatment options, and the one that matches the risk score is selected.

The options are:

- No Action: Only send an email to inform of no action
- Inform: Send an email informing a team to investigate this deviation
- Raise Access Request: Automatically raise an access request to add/remove access according to it's deviation

### Treatment

The treatment process takes the specified treatment and performs it.

## Testing

The unit tests included in the components require the installation of pytest to run.

`pip install pytest`

Tests need to be ran on an installation of Bravura Security Identity and the tests must be run from the component\Custom folder.
