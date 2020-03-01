from ipaddress import IPv4Address
from router.get_router import get_router_ipv4
from subprocess import run


def insert_router_ipv4(insert: [(IPv4Address, str, IPv4Address, int)], interface: str, host: str, port: int, user: str,
                       key: str, debug: bool = False):
    """
    This function insert IPv4 on the router

    :param insert: The list of IPs, MACs to insert
    :type insert: [(IPv4Address, str, IPv4Address, int)]
    :param interface: The interface of IPs
    :type interface: str
    :param host: The SSH host of the router
    :type host: str
    :param port: The SSH port of the router
    :type port: int
    :param user: The SSH user of the router
    :type port: str
    :param key: The SSH key of the router
    :type key: str
    :param debug: Disable commit on database
    :type debug: bool
    """

    ipl = get_router_ipv4(host, port, user, key)

    for i in insert:
        if ((i[0] not in ipl) or not (ipl[ipl.find(i[0]):5].replace(" ", ""))) and (i[1] not in ipl):
            cmd = ["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", port, f"/ip arp add address={i[0]} mac-address={i[1]} interface={interface}".replace("'", "")]
            if not debug:
                run(cmd)
            else:
                print(cmd)
