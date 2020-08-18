<p align="center">
  <a href="https://aiqfome.com/" rel="noopener" target="_blank"><img width="150" src="https://www.suafranquia.com/views/sources/images/franquias/logos/271b399b0a004c781779ec805e8d7ab7.png" alt="aiqfome logo"></a></p>
</p>

<h1 align="center">aiqDocTests</h1>

<p align="">AiqDocTests A framework to validate request/response's json and create documentation for applications maintained by the devs of the <a href="https://aiqfome.com/">most greedy-gut app on the internet</a>!</p>

<p align="center">
  <a href="https://github.com/aiqfome" style="text-decoration:none" target="_blank">
    <img alt="Made by AiqFome" src="https://img.shields.io/badge/made%20by-aiqfome-blueviolet">
  </a>

  <img alt="Last Commit" src="https://img.shields.io/github/last-commit/aiqfome/aiqDocTests">

  <img alt="Contributors" src="https://img.shields.io/github/contributors/aiqfome/aiqDocTests">

  <img alt="License" src="https://img.shields.io/github/license/aiqfome/aiqDocTests">
</p>

---

### Install with pip3

`pip3 install aiqDocTests`

### Init in the project folder

`aiqdoctests --init`

Will be created the folder **data_scructures_io** and **static**.

In the **data_scructures_io**, is the json files to test the request. [Example](https://github.com/aiqfome/aiqDocTests-example/blob/master/data_structures_io/transfers.json)

We using [Cerberus](https://docs.python-cerberus.org/en/stable/) to validate the structure. So if any valid in the json response is a name, type or don't send. Will occurs a exception in tests.

In the **static** folder, will be the json file to [Swagger](https://swagger.io), with this file you can any package in any language what you want to read.
This swagger.json is generate, so every time that you run the command `aiqdoctests -g` in the folder this file will be update.

### The _.aiqdoctests.config_ file

This json file is for configuration, so the name folders and other things can be personalizable.

#### docs_url
with the command `aiqdoctests --docs` will be up un flask server in the port 3000 and read the swagger file, this value is for which url will run. **_default: localhost:3000/docs_**

#### save_file_swagger
The name file generate to swagger. **_default: swagger.json_**

#### data_structures_folder
The name folder that are the data scructures for requests. **_default: data_structures_io_**

#### tests_folder
The name folder that will be the tests. **_default: tests_**

#### tests_before_cmd
Sometimes in the project, we wanna run command/script before start the tests, example create the tables in the bd. Will run this command before start the tests.

#### tests_between_cmd
This command is for run between tests, in the **tearDown**, so **after** run a test, this is for a script or migration that you want to run for clean the bd for example.

#### swagger
The header for swagger file.

### For more information

For more you can see in the example (https://github.com/aiqfome/aiqDocTests-example)

---

Relax, this documentation is still in construction :construction_worker:

Any doubt create a issue.

---


Made with :pizza: & :hearts:! Enjoy it!