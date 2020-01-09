#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#slims_import.py

import sys
import click
import requests
import json
import datetime

@click.command()
@click.option('--slims_url', default="https://slims-lisp.epfl.ch/rest/rest", help='Slims REST URL.', required=True)
@click.option('--proj', help='Project name.', required=False)
@click.option('--exp', help='Experiment name.', required=True)
@click.option('--step', default='data_collection', help='Experiment step name.', required=True)
@click.option('-a', '--attm', help='Attachment name.', required=True)
@click.option('-o', '--output', help='Output file name.', required=False)
@click.option('-u', '--username', prompt="User", help='User name.', required=True)
@click.option('-p', '--pwd', prompt="Password", hide_input=True, help='Password.', required=True)
def get_attachment(slims_url, proj, exp, step, attm, output, username, pwd):
    """Download a file from a slims experiment attachment step."""

    if output is None:
      output = attm

    project = requests.get(slims_url+"/Project/advanced",
                             auth=(username, pwd),
                             headers={"Content-Type":"application/json"},
                             json={"criteria":{"operator":"and",
                                               "criteria":[
                                                   {"fieldName":"prjc_name",
                                               "operator":"equals",
                                               "value":proj},
                                                   {"fieldName":"user_userName",
                                               "operator":"equals",
                                               "value":username}
                                               ]}
                                  })
    if len(project.json()["entities"]) > 1:
        sys.exit("Multiple projects found for"+proj+". Make sure projects names are unique.")

    experiment_run = requests.get(slims_url+"/ExperimentRun/advanced",
                             auth=(username, pwd),
                             headers={"Content-Type":"application/json"},
                             json={"criteria":{"operator":"and",
                                               "criteria":[
                                                   {"fieldName":"xprn_fk_project",
                                               "operator":"equals",
                                               "value":project.json()["entities"][0]["pk"]},
                                                   {"fieldName":"xprn_name",
                                               "operator":"equals",
                                               "value":exp},
                                                   {"fieldName":"user_userName",
                                               "operator":"equals",
                                               "value":username}
                                               ]}
                                  })
    if len(experiment_run.json()["entities"]) > 1:
        sys.exit("Multiple experiments found for"+exp+". Make sure experiments names are unique.")

    experiment_step = requests.get(slims_url+"/ExperimentRunStep/advanced",
                             auth=(username, pwd),
                             headers={"Content-Type":"application/json"},
                             json={"criteria":{"operator":"and",
                                               "criteria":[
                                                   {"fieldName":"xprs_fk_experimentRun",
                                               "operator":"equals",
                                               "value": experiment_run.json()['entities'][0]['pk']},
                                                   {"fieldName":"xpst_type",
                                               "operator":"equals",
                                               "value": "ATTACHMENT_STEP"},
                                                   {"fieldName":"xpst_name",
                                               "operator":"equals",
                                               "value": step}
                                                          ]}
                                  })

    if len(experiment_step.json()["entities"]) > 1:
        sys.exit("Multiple steps found for"+exp+"/"+step+". Make sure steps names are unique.")

    attachment = requests.get(slims_url+"/Attachment/advanced",
                             auth=(username, pwd),
                             headers={"Content-Type":"application/json"},
                             json={"criteria":{"operator":"and",
                                               "criteria":[
                                                   {"fieldName":"attm_name",
                                               "operator":"equals",
                                               "value":attm},
                                                   {"fieldName":"user_userName",
                                               "operator":"equals",
                                               "value":username}
                                                          ]}
                                  })

    attachment = [[{"attm_file_filename":e1["value"], "pk":e0["pk"]} for e1 in e0["columns"] if e1["name"] == "attm_file_filename"][0] for e0 in attachment.json()["entities"]]

    attachment_link = requests.get(slims_url+"/AttachmentLink/advanced",
                             auth=(username, pwd),
                             headers={"Content-Type":"application/json"},
                             json={"criteria":{"operator":"and",
                                               "criteria":[
                                                   {"fieldName":"atln_recordTable",
                                               "operator":"equals",
                                               "value":"ExperimentRunStep"},
                                                   {"fieldName":"atln_recordPk",
                                               "operator":"equals",
                                               "value":experiment_step.json()['entities'][0]['pk']}
                                                          ]}
                                  })

    attachment_link_pk = [e2[0] for e2 in [[e1["value"] for e1 in e0["columns"] if e1["name"] == "atln_fk_attachment" and (e1["value"] in [e2["pk"] for e2 in attachment])] for e0 in attachment_link.json()["entities"]] if e2]

    if len(attachment_link_pk) > 1:
        sys.exit("Multiple attachments found for "+attm+" in "+exp+"/"+step+". Make sure attachments names are unique.")

    # Download the attachement
    with requests.get(slims_url+"/repo/"+str(attachment_link_pk[0]),
                      auth=(username, pwd),
                      stream=True) as r:
        r.raise_for_status()
        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    # Save metadata
    metadata = {"url":slims_url+"/repo/"+str(attachment_link_pk[0]),
            "creator":username,
            "project_name":proj,
            "experiment_name":exp,
            "step_name":step,
            "attachment_name":attm,
            "attachment_file_filename":[e["attm_file_filename"] for e in attachment if e["pk"] == attachment_link_pk[0]][0],
            "file_name":output,
            "created":datetime.datetime.now(datetime.timezone.utc).isoformat(sep='T')}

    with open(output+"_metadata.txt", "w") as f:
        json.dump(metadata, f, indent=2)

if __name__ == '__main__':
    get_attachment()
