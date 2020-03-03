from ipaddress import IPv4Address
from sys import stderr
from pymysql import Connect


def insert_whmcs_ipv4(insert: [(IPv4Address, str, IPv4Address, int)], interface: str, db: Connect, debug: bool = False,
                      verbose: bool = False):
    """
    This function insert given IPs and MACs to WHMCS

    :param insert: The list of IPs, MACs to insert
    :type insert: [(IPv4Address, str, IPv4Address, int)]
    :param interface: The interface of IPs
    :type interface: str
    :param db: The database connection of WHMCS
    :type db: pymysql.Connect
    :param debug: Disable commit on database
    :type debug: bool
    :param verbose: Print actions on database
    :type verbose: bool
    """
    cursor = db.cursor()
    # Get gateway
    gateway = insert[0][0]
    del insert[0]
    # Get vlan if given
    if interface[:4] == "vlan":
        try:
            vlan = int(interface[4:])
        except ValueError:
            raise ValueError("Invalid vlan !")
    else:
        vlan = "null"

    # For every IP to insert
    for i in insert:
        if i[1]:
            cmd = f"INSERT INTO mg_proxmox_addon_ip (ip, type, mac_address, subnet_mask, cidr, sid gateway, tag) " \
                        f"VALUES ('{i[0]}', 'IPv4', '{i[1]}', '{i[2]}', {i[3]}, 0, '{gateway}', {vlan})"
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
