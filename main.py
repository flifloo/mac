from pymysql import connect
from argparse import ArgumentParser
from os.path import isfile
from json import dump, load
from whmcs.get_whmcs import get_whmcs_ipv4, get_whmcs_mac
from whmcs.insert_whmcs import insert_whmcs_ipv4
from whmcs.remove_whmcs import remove_whmcs_ipv4
from router.insert_router import insert_router_ipv4, insert_router_ipv6
from router.remove_router import remove_router_ipv4, remove_router_ipv6
from ip.ipv4 import ipv4

if not isfile("config.json"):
    with open("config.json", "w") as config:
        data = {"database": {"host": "", "user": "", "password": "", "name": ""},
                "ssh": {"host": "", "port": 22, "user": "", "key": "", "options": []},
                "interface": {"default": ""},
                "IPv6": {"template": ""}}
        dump(data, config)
    print("Config file created, please fill it")
    exit()
with open("config.json", "r") as config:
    conf = load(config)
DB_HOST = conf["database"]["host"]
DB_USER = conf["database"]["user"]
DB_PASS = conf["database"]["password"]
DB_NAME = conf["database"]["name"]

SSH_HOST = conf["ssh"]["host"]
SSH_PORT = conf["ssh"]["port"]
SSH_USER = conf["ssh"]["user"]
SSH_KEY = conf["ssh"]["key"]
SSH_OPTIONS = conf["ssh"]["options"]

IPV6_TEMPLATE = conf["IPv6"]["template"]

DEFAULT_INTERFACE = conf["interface"]["default"]

pars = ArgumentParser()
pars.add_argument("interface", help="Interface of IPs")
pars.add_argument("prefix", help="IPs prefix")
pars.add_argument("-d", "--debug", help="Any consequence and verbose", action="store_true")
pars.add_argument("-v", "--verbose", help="More output", action="store_true")
pars.add_argument("--delete", help="Delete IPv4 and v6", action="store_true")
args = pars.parse_args()

debug = False
if args.debug:
    debug = True
    print("DEBUG MOD ACTICATED !")
if args.verbose:
    print("Verbose enabled")

# DB connection
db = connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)

ipl = get_whmcs_ipv4(db)
macl = get_whmcs_mac(db)

# Get list of ip, mac and subnet_mask to add
out = ipv4(args.prefix, ipl, macl)

# Insert the list
if not args.delete:
    insert_whmcs_ipv4(out, args.interface, db, debug, args.verbose)
    insert_router_ipv4(out, args.interface, SSH_HOST, SSH_PORT, SSH_USER, SSH_KEY, debug, args.verbose, SSH_OPTIONS)
    insert_router_ipv6(out, IPV6_TEMPLATE, args.interface, SSH_HOST, SSH_PORT, SSH_USER, SSH_KEY, debug, args.verbose, SSH_OPTIONS)
else:
    remove_whmcs_ipv4(out, db, debug, args.verbose)
    remove_router_ipv4(out, SSH_HOST, SSH_PORT, SSH_USER, SSH_KEY, debug, args.verbose, SSH_OPTIONS)
    remove_router_ipv6(out, IPV6_TEMPLATE, SSH_HOST, SSH_PORT, SSH_USER, SSH_KEY, debug, args.verbose, SSH_OPTIONS)
