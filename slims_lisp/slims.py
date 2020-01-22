import os
import sys
import json
import requests
import datetime
import base64

class Slims(object):

    def __init__(self, url, username, pwd):
        self.url = url
        self.username = username
        self.pwd = pwd

    def get(self, table, **kwargs):
        if "response" not in kwargs.keys():
            response = []
        else:
            response = kwargs["response"]
            del kwargs["response"]
        response.append(requests.get(self.url + "/" + table,
                auth = (self.username, self.pwd),
                **kwargs
            )
        )
        return response[0]

    def post(self, table, **kwargs):
        if "response" not in kwargs.keys():
            response = []
        else:
            response = kwargs["response"]
            del kwargs["response"]
        response.append(requests.post(self.url + "/" + table,
                auth = (self.username, self.pwd),
                **kwargs
            )
        )
        return response[0]
    
    def get_project(self, **kwargs):
        criteria = [{"fieldName":key,
                "operator":"equals",
                "value":value}
                for key, value in kwargs.items()]

        return self.get(table = "Project/advanced",
                headers = {"Content-Type":"application/json"},
                json = {"criteria":{"operator":"and",
                        "criteria":criteria
                }
            }
        )

    def get_experiment(self, **kwargs):
        criteria = [{"fieldName":key,
                "operator":"equals",
                "value":value}
                for key, value in kwargs.items()]

        return self.get(table = "ExperimentRun/advanced",
                headers = {"Content-Type":"application/json"},
                json = {"criteria":{"operator":"and",
                        "criteria":criteria
                }
            }
        )

    def get_experiment_step(self, active, **kwargs):
        criteria = [{"fieldName":key,
                "operator":"equals",
                "value":value}
                for key, value in kwargs.items()]

        if active is not None and active != "both":
            criteria.append({"fieldName":"xprs_active",
                "operator":"equals",
                "value":active})

        return self.get(table = "ExperimentRunStep/advanced",
                headers = {"Content-Type":"application/json"},
                json = {"criteria":{"operator":"and",
                        "criteria":criteria
                }
            }
        )

    def get_attachment(self, linked, **kwargs):
        criteria = [{"fieldName":key,
                "operator":"equals",
                "value":value}
                for key, value in kwargs.items()]

        if linked is not None and linked != "both":
            criteria.append({"fieldName":"attm_linkCount",
                "operator":"greaterThan",
                "value":0})

        return self.get(table = "Attachment/advanced",
                headers = {"Content-Type":"application/json"},
                json = {"criteria":{"operator":"and",
                        "criteria":criteria
                }
            }
        )

    def get_attachment_link(self, **kwargs):
        criteria = [{"fieldName":key,
                "operator":"equals",
                "value":value}
                for key, value in kwargs.items()]

        return self.get(table = "AttachmentLink/advanced",
                headers = {"Content-Type":"application/json"},
                json = {"criteria":{"operator":"and",
                        "criteria":criteria
                }
            }
        )

    def download_attachment(self, proj, exp, step, active, attm, linked, output):
        """Download a file from a slims experiment attachment step."""

        if active is None:
            active = "true"
        active = active.lower()
        if linked is None:
            linked = "true"
        linked = linked.lower()
        if output is None:
            output = attm

        # Retrieve Project
        kwargs = {"xprn_name":exp,
            "user_userName":self.username,
            "value":exp
        }

        if proj:
            project = self.get_project(prjc_name = proj, user_userName = self.username)

            if len(project.json()["entities"]) > 1:
                sys.exit("Multiple projects found with name '" + proj +
                    "'. Make sure projects names are unique."
                )
            elif len(project.json()["entities"]) == 0:
                sys.exit("No project found with name '" + proj + "'.")

            kwargs.update({"xprn_fk_project":project.json()["entities"][0]["pk"]})

        experiment_run = self.get_experiment(**kwargs)
    
        if len(experiment_run.json()["entities"]) > 1:
            sys.exit("Multiple experiments found with name '" + exp +
                "'. Make sure experiments names are unique."
            )
        elif len(experiment_run.json()["entities"]) == 0:
            sys.exit("No experiment found with name '" + exp + "'.")

        # Retrieve ExperimentRunStep
        experiment_step = self.get_experiment_step(active = active,
            xprs_fk_experimentRun = experiment_run.json()['entities'][0]['pk'],
            xpst_type = "ATTACHMENT_STEP",
            xpst_name = step)

        if len(experiment_step.json()["entities"]) > 1:
            sys.exit("Multiple steps found with name '" + step +
                "' in experiment '" + exp +
                "'. Make sure steps names are unique."
            )
        elif len(experiment_step.json()["entities"]) == 0:
            sys.exit("No step found with name '" + step +
                "' in experiment '" + exp + "'."
            )

        # Retrieve Attachment
        attachment = self.get_attachment(linked = linked,
            attm_name = attm,
            user_userName = self.username)

        attachment = [
            [{"attm_file_filename":e1["value"], "pk":e0["pk"]}
                for e1 in e0["columns"]
                if e1["name"] == "attm_file_filename"
            ][0]
            for e0 in attachment.json()["entities"]
        ]

        # Retrieve Attachment link
        attachment_link = self.get_attachment_link(atln_recordTable = "ExperimentRunStep",
            atln_recordPk = experiment_step.json()["entities"][0]["pk"])

        attachment_link_pk = [
            e2[0] for e2 in [[e1["value"]
                    for e1 in e0["columns"]
                    if e1["name"] == "atln_fk_attachment"
                    and (e1["value"] in [e2["pk"] for e2 in attachment])
                ]
                for e0 in attachment_link.json()["entities"]
            ]
            if e2
        ]

        if len(attachment_link_pk) > 1:
            sys.exit("Multiple attachments found with name '" + attm +
                "' in experiment '" + exp +
                "' step '" + step +
                "'. Make sure attachments names are unique."
            )
        elif len(attachment_link_pk) == 0:
            sys.exit("No attachment found with name '" + attm +
                "' in experiment '" + exp +
                "' step '" + step + "'."
                )

        # Download the attachement
        response = []
        with self.get(table = "repo/" + str(attachment_link_pk[0]),
            response = response,
            stream = True) as r:
            with open(output, "wb") as f:
                for chunk in r.iter_content(chunk_size = 8192):
                    if chunk:
                        f.write(chunk)

        # Save metadata
        metadata = {"url":self.url + "/repo/" + str(attachment_link_pk[0]),
            "creator":self.username,
            "project_name":proj,
            "experiment_name":exp,
            "step_name":step,
            "attachment_name":attm,
            "attachment_file_filename":[
                e["attm_file_filename"]
                for e in attachment
                if e["pk"] == attachment_link_pk[0]
            ][0],
            "file_name":output,
            "created":datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(sep='T')
        }

        with open(output + "_metadata.txt", "w") as f:
            json.dump(metadata, f, indent=2)

        return response[0]


    def upload_attachment(self, proj, exp, step, active, attm, file):
        """Upload a file to a slims experiment attachment step."""

        if active is None:
            active = "true"
        active = active.lower()
        if attm is None:
            attm = os.path.basename(file)

        # Retrieve Project
        kwargs = {"xprn_name":exp,
            "user_userName":self.username,
            "value":exp
        }

        if proj:
            project = self.get_project(prjc_name = proj, user_userName = self.username)

            if len(project.json()["entities"]) > 1:
                sys.exit("Multiple projects found with name '" + proj +
                    "'. Make sure projects names are unique."
                )
            elif len(project.json()["entities"]) == 0:
                sys.exit("No project found with name '" + proj + "'.")

            kwargs.update({"xprn_fk_project":project.json()["entities"][0]["pk"]})

        experiment_run = self.get_experiment(**kwargs)
    
        if len(experiment_run.json()["entities"]) > 1:
            sys.exit("Multiple experiments found with name '" + exp +
                "'. Make sure experiments names are unique."
            )
        elif len(experiment_run.json()["entities"]) == 0:
            sys.exit("No experiment found with name '" + exp + "'.")

        # Retrieve ExperimentRunStep
        experiment_step = self.get_experiment_step(active = active,
            xprs_fk_experimentRun = experiment_run.json()["entities"][0]["pk"],
            xpst_type = "ATTACHMENT_STEP",
            xpst_name = step)

        if len(experiment_step.json()["entities"]) > 1:
            sys.exit("Multiple steps found with name '" + step +
                "' in experiment '" + exp +
                "'. Make sure steps names are unique."
            )
        elif len(experiment_step.json()["entities"]) == 0:
            sys.exit("No step found with name '" + step +
                "' in experiment '" + exp + "'."
            )

        with open(file, "rb") as f:
            response = self.post(table = "/repo",
                    headers = {"Content-Type":"application/json"},
                    json = {"atln_recordTable":"ExperimentRunStep",
                    "atln_recordPk":experiment_step.json()["entities"][0]['pk'],
                    "attm_name":attm,
                    "contents":base64.b64encode(f.read()).decode("utf-8")},
                    stream = True
            )

        return response