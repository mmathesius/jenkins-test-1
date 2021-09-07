#!/usr/bin/python3

import argparse
import datetime
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

    for compose_type in COMPOSE_TYPES:
        logging.debug(">> {} REPORT GOES HERE <<<".format(compose_type))

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

        logging.info("Latest successful {type} compose {id} date: {date}".format(type=compose_type, id=latest_composeid, date=latest_composedate))

        parsed_date = datetime.datetime.strptime(latest_composedate, "%Y%m%d")
        logging.debug("Parsed date: {date}".format(date=parsed_date.date()))

        failed_days = (today - parsed_date.date()).days
        logging.info("Latest successful {type} compose {id} was {ago} days ago.".format(type=compose_type, id=latest_composeid, ago=failed_days))


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
