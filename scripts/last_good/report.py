#!/usr/bin/python3

import argparse
import datetime
import jinja2
import logging
import os
import pprint
import requests

COMPOSE_TOPURL = "https://odcs.stream.rdu2.redhat.com/composes"
COMPOSE_TYPES = ["production", "development"]
COMPOSE_RELEASE = "CentOS-Stream"

SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))


def report():
    today = datetime.date.today()

    results = {}
    results["today"] = str(today)
    results["release"] = COMPOSE_RELEASE
    results["compose_types"] = {}

    for compose_type in COMPOSE_TYPES:
        logging.debug("Working on compose_type {}".format(compose_type))

        latest_composeurl = "{topurl}/{type}/latest-{release}".format(
            topurl=COMPOSE_TOPURL, type=compose_type, release=COMPOSE_RELEASE
        )
        composeinfo_url = "{composeurl}/compose/metadata/composeinfo.json".format(
            composeurl=latest_composeurl
        )
        logging.debug("composinfo URL: {}".format(composeinfo_url))

        resp = requests.get(composeinfo_url, verify=False)
        if not resp:
            logging.error("Failed to fetch composeinfo from {}".format(composeinfo_url))
            sys.exit(1)

        try:
            latest_composeinfo = resp.json()
            logging.debug("resp.json()={}".format(pprint.pformat(latest_composeinfo)))
        except ValueError:
            logging.exception("composeinfo metadata is not in JSON format")
            sys.exit(1)

        latest_composeid = latest_composeinfo["payload"]["compose"]["id"]
        latest_composedate = latest_composeinfo["payload"]["compose"]["date"]

        logging.info(
            "Latest successful {type} compose {id} date: {date}".format(
                type=compose_type, id=latest_composeid, date=latest_composedate
            )
        )

        parsed_date = datetime.datetime.strptime(latest_composedate, "%Y%m%d").date()
        logging.debug("Parsed date: {date}".format(date=parsed_date))

        failed_days = (today - parsed_date).days
        logging.info(
            "Latest successful {type} compose {id} was {age} days ago.".format(
                type=compose_type, id=latest_composeid, age=failed_days
            )
        )

        real_composeurl = "{topurl}/{type}/{id}".format(
            topurl=COMPOSE_TOPURL, type=compose_type, id=latest_composeid
        )

        results["compose_types"][compose_type] = {
            "id": latest_composeid,
            "link": real_composeurl,
            "date": str(parsed_date),
            "age": failed_days,
        }

    print("results = {}".format(pprint.pformat(results)))

    render(results, tmpl_path=os.path.join(SCRIPTPATH, "templates"))


def render(results, tmpl_path="templates", output_path="output", fmt="all"):
    os.makedirs(output_path, exist_ok=True)

    j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_path))
    templates = j2_env.list_templates(extensions="j2")
    logging.debug("Templates to render found in {}: {}".format(tmpl_path, templates))
    if fmt != "all":
        fmtlist = fmt.split(",")
        templates = [name for name in templates if name.split(".")[-2] in fmtlist]
    for tmpl_name in templates:
        tmpl = j2_env.get_template(tmpl_name)
        tmpl.stream(results=results).dump(
            os.path.join(
                output_path,
                tmpl_name[:-3],
            )
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug logging",
        action="store_true",
    )

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    report()
