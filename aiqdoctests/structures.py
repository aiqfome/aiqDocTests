import os
import json
import sys

from cerberus import Validator
import requests
from http import HTTPStatus
from unittest import TestCase
from shutil import copyfile
import unittest

unittest.util._MAX_LENGTH = 2000

AIQDOCTESTS_DATA_FOLDER = "AIQDOCTESTS_DATA_FOLDER"
AIQDOCTESTS_CMD_TEARDOWN = "AIQDOCTESTS_CMD_TEARDOWN"


class StructureIO:
    def __init__(self, file):
        self.importScructure(file)

    def getResponseValidator(self, http_verb, code):
        response = self.responses[http_verb.lower()][str(code)]
        if response is None:
            return None
        return response["properties"]

    def getContentValidator(self, content):
        c = None
        if self.__dict__.get("requestBody", None):
            c = self.requestBody["content"][content]["properties"]
        return c

    @classmethod
    def convertToSwagger(cls, properties):
        ret = {}
        ret["content"] = {}
        ret["content"]["application/json"] = {}
        ret["content"]["application/json"]["schema"] = {}
        ret["content"]["application/json"]["schema"]["type"] = "object"
        ret["content"]["application/json"]["schema"][
            "properties"
        ] = StructureIO.convertObject(properties)

        return ret

    @classmethod
    def convertObject(cls, properties):
        json = {}
        if properties.get("type", None):
            if properties["type"] == "dict":
                json["type"] = "object"
                json["properties"] = StructureIO.convertObject(properties["schema"])
            elif properties["type"] == "list":
                json["type"] = "array"
                json["items"] = properties["schema"]
            else:
                json["type"] = properties["type"]
            return json

        for tag in properties:
            json[tag] = {}
            if properties[tag]["type"] == "dict":
                json[tag]["type"] = "object"
                json[tag]["properties"] = StructureIO.convertObject(
                    properties[tag]["schema"]
                )
            elif properties[tag]["type"] == "list":
                json[tag]["type"] = "array"
                json[tag]["items"] = StructureIO.convertObject(
                    properties[tag]["schema"]
                )
            elif properties[tag]["type"] == "float":
                json[tag]["type"] = "number"
                json[tag]["format"] = "double"
            else:
                json[tag]["type"] = properties[tag]["type"]
        return json

    def getSwaggerJson(self):
        json = {}
        json[self.url] = {}
        requestBody = {}
        if self.__dict__.get("summary", None):
            json[self.url]["summary"] = self.summary
        if self.__dict__.get("requestBody", None):
            requestBody = self.requestBody.copy()
            requestBody["content"] = {}
            for content in self.requestBody["content"]:
                requestBody["content"][content] = {}
                requestBody["content"][content]["schema"] = {}
                requestBody["content"][content]["schema"]["type"] = "object"
                requestBody["content"][content]["schema"][
                    "required"
                ] = self.requestBody["content"][content]["required"]
                requestBody["content"][content]["schema"][
                    "properties"
                ] = StructureIO.convertObject(
                    self.requestBody["content"][content]["properties"]
                )

        for method in self.responses:
            json[self.url][method] = {}
            if requestBody:
                json[self.url][method]["requestBody"] = requestBody
            if self.__dict__.get("parameters", None):
                json[self.url][method]["parameters"] = self.parameters
            if self.__dict__.get("tags", None):
                json[self.url][method]["tags"] = self.tags
            if self.__dict__.get("consumes", None):
                json[self.url][method]["consumes"] = self.consumes
            if self.__dict__.get("produces", None):
                json[self.url][method]["produces"] = self.produces
            json[self.url][method]["responses"] = {}
            for code in self.responses[method]:
                if self.responses[method][code] is None:
                    continue
                json[self.url][method]["responses"][code] = {}
                json[self.url][method]["responses"][code][
                    "description"
                ] = self.responses[method][code]["description"]
                json[self.url][method]["responses"][code].update(
                    StructureIO.convertToSwagger(
                        self.responses[method][code]["properties"]
                    )
                )
        return json

    def method(self, method=None):
        if method is None and len(self.responses.keys()) == 1:
            return [key for key in self.responses][0]
        if method is None:
            raise Exception(
                "Exist more than one method, impossible situation! Methods: %s"
                % self.responses
            )
        if method is not None:
            http_verb = method.lower()
            if http_verb in self.responses:
                return http_verb
        raise Exception(
            "Impossible situation! I don't know what to do method: %s Methods in class: %s"
            % (http_verb, self.responses)
        )

    def importScructure(self, file):

        if not file:
            raise Exception("File is Null, impossible import")
        try:
            self.__dict__ = self.loadJsonScructure(file)
            self.name_file = file
        except Exception as ex:
            raise Exception("Error in file %s\n%s" % (file, ex))

    def loadJsonScructure(self, json_scructure):
        script_dir = os.getcwd()
        rel_path = "%s/%s.json" % (os.getenv(AIQDOCTESTS_DATA_FOLDER), json_scructure,)
        json_scructure_path = os.path.join(script_dir, rel_path)

        with open(json_scructure_path, "r") as file:
            json_scructure = file.read()

        return json.loads(json_scructure)


class Config:
    def __init__(self):
        self.importConfig(".aiqdoctests.config")
        self.save_folder_swagger = "static"
        os.environ[AIQDOCTESTS_DATA_FOLDER] = self.data_structures_folder
        os.environ[AIQDOCTESTS_CMD_TEARDOWN] = self.tests_between_cmd

    def importConfig(self, file):
        if not file:
            raise Exception("File is Null, impossible import")
        try:
            self.__dict__ = self.loadJsonScructure(file)
        except:
            raise Exception("Error in file %s" % file)

    def loadJsonScructure(self, json_scructure):
        with open(json_scructure, "r") as file:
            json_scructure = file.read()

        return json.loads(json_scructure)

    def runTestsDocker(self, wait=False):
        cmd = "sh -c "
        if wait:
            copyfile(
                os.path.join(
                    os.path.dirname(sys.modules["aiqdoctests"].__file__), "wait"
                ),
                os.path.join(os.getcwd(), "/wait"),
            )
            os.system("chmod +x /wait")
            cmd += "'/wait' && "
        if self.__dict__.get("tests_before_cmd", None):
            cmd += "%s && " % self.tests_before_cmd
        return os.system(
            "%s python3 -m unittest discover -v -s %s" % (cmd, self.tests_folder)
        )

    def path_swagger_file(self):
        return "%s/%s" % (self.save_folder_swagger, self.save_file_swagger)

    def saveSwaggerJson(self):
        if not os.path.exists(self.save_folder_swagger):
            os.mkdir(self.save_folder_swagger)

        with open(self.path_swagger_file(), "w+") as file:
            file.write(json.dumps(self.swagger, indent=3))

        return self.path_swagger_file()

    def returnJson(self, json_scructure_path):
        with open(json_scructure_path, "r") as file:
            json_scructure = file.read()

        return json.loads(json_scructure)

    def jsonFromStructure(self, json_scructure_path):
        s = StructureIO(json_scructure_path)
        return s.getSwaggerJson()

    def generateSwagger(self):
        if not os.path.exists(self.data_structures_folder):
            os.mkdir(self.data_structures_folder)
        json_files = [
            pos_json.replace(".json", "")
            for pos_json in os.listdir(self.data_structures_folder)
            if pos_json.endswith(".json")
        ]
        self.swagger["paths"] = {}
        for json in json_files:
            self.swagger["paths"].update(self.jsonFromStructure(json))

        return self.saveSwaggerJson()


class AiqTest(TestCase):
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.maxDiff = None

    def setStructure(self, file):
        self.structure = StructureIO(file)

    def url(self, parameters={}):
        url = self.structure.url
        for key in parameters:
            url = url.replace("{%s}" % key, str(parameters[key]))
        return os.getenv("BASE_URL") + url

    def http_verb(self, method=None):
        return self.structure.method(method)

    def assertResponseStructure(
        self,
        http_code,
        method=None,
        headers=None,
        payload={},
        content="application/json",
        parameters_url={},
    ):

        contentValidator = Validator()
        try:
            contentValidator.schema = self.structure.getContentValidator(content)
        except Exception as ex:
            self.fail(
                "Not defined content for %s - in file %s\nError: %s"
                % (content, self.structure.name_file, ex)
            )
        http_verb = self.http_verb(method)
        r = getattr(requests, http_verb)(
            url=self.url(parameters_url), headers=headers, json=payload
        )
        self.assertEqual(http_code, r.status_code)
        responseValidator = Validator()
        try:
            responseValidator.schema = self.structure.getResponseValidator(
                http_verb, http_code
            )
        except Exception as ex:
            self.fail(
                "Not defined the schema for %s - %d in file %s\nError: %s"
                % (http_verb, http_code, self.structure.name_file, ex)
            )

        try:
            j = r.json()
        except:
            return r

        if (responseValidator.schema and not responseValidator.validate(j)) or (
            contentValidator.schema and not contentValidator.validate(payload)
        ):
            self.fail(
                "content_errors:%s\nresponse_errors:%s"
                % (contentValidator.errors, responseValidator.errors,)
            )
        return r

    def assertOK(self, method=None, headers=None, payload=None, parameters_url={}):
        return self.assertResponseStructure(
            HTTPStatus.OK.value,
            method=method,
            headers=headers,
            payload=payload,
            parameters_url=parameters_url,
        )

    def clearTest(self):
        os.system(os.getenv(AIQDOCTESTS_CMD_TEARDOWN))

    def tearDown(self):
        super().tearDown()
        try:
            if self.http_verb() != "get":
                self.clearTest()
        except:
            self.clearTest()
