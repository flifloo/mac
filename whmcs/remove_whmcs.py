from ipaddress import IPv4Address
from sys import stderr
from pymysql import Connect


def remove_whmcs_ipv4(remove: [(IPv4Address, str, IPv4Address, int)], db: Connect, debug: bool = False, verbose: bool = False):
    """
    This function remove IPv6 on the router

    :param remove: The list of IPs, MACs to remove
    :type remove: [(IPv4Address, str, IPv4Address, int)]
    :param db: The database connection of WHMCS
    :type db: pymysql.Connect
    :param debug: Disable commit on database
    :type debug: bool
    :param verbose: Print each command on router
    :type verbose: bool
    """

    cursor = db.cursor()

    for i in remove:
        cmd = f"DELETE FROM mg_proxmox_addon_ip WHERE ip = '{i[0]}'"
        try:
            cursor.execute(cmd)
        except Exception as e:
            print(cmd, file=stderr)
            raise e
        if debug or verbose:
            print(cmd)

    cursor.close()

    # Commit to the DB
    if not debug:
        try:
            print("Commit to DB...")
            db.commit()
        except Exception as e:
            raise e
        else:
            print("Commited to DB")
