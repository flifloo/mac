from ipaddress import IPv4Address
from router.get_router import get_router_ipv4, get_router_mac
from ip.ipv6 import link_local
from subprocess import run


def insert_router_ipv4(insert: [(IPv4Address, str, IPv4Address, int)], interface: str, host: str, port: int, user: str,
                       key: str, debug: bool = False, verbose: bool = False, ssh_options: list = []):
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
    :param debug: Disable command on router
    :type debug: bool
    :param verbose: Print each command on router
    :type verbose: bool
    :param ssh_options: SSH optionals arguments
    :type ssh_options: list
    """

    ipl = get_router_ipv4(host, port, user, key, ssh_options)
    macl = get_router_mac(host, port, user, key, ssh_options)

    print("Start insert IPv4 on router")
    for i in insert:
        if i[1]:
            if (i[0] not in ipl) and (i[1] not in macl):
                cmd = ["ssh", "-i", key, "-o", "StrictHostKeyChecking no"] + ssh_options + [f"{user}@{host}", "-p", str(port),
                       f"/ip arp add address={i[0]} mac-address={i[1]} interface={interface}"]
                if not debug:
                    run(cmd)
                if debug or verbose:
                    print(cmd)
    print("Insert IPv4 on router done")


def insert_router_ipv6(insert: [(IPv4Address, str, IPv4Address, int)], ipv6: str, interface: str, host: str, port: int, user: str,
                       key: str, debug: bool = False, verbose: bool = False, ssh_options: list = []):
    """
    This function insert IPv6 on the router

    :param insert: The list of IPs, MACs to insert
    :type insert: [(IPv4Address, str, IPv4Address, int)]
    :param ipv6: The IPV6 template
    :type ipv6: str
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
    :param verbose: Print each command on router
    :type verbose: bool
    :param ssh_options: SSH optionals arguments
    :type ssh_options: list
    """

    print("Start insert IPv6 on router")
    for i in insert:
        if i[1]:
            ip = ipv6.format(str(i[0]).split(".")[-1])
            gateway = link_local(i[1])
            cmd = ["ssh", "-i", key, "-o", "StrictHostKeyChecking no"] + ssh_options + [f"{user}@{host}", "-p", str(port),
                   f"/ipv6 route add dst-address={ip} gateway={gateway}%{interface}"]
            if not debug:
                run(cmd)
            if debug or verbose:
                print(cmd)
    print("Insert IPv6 on router done")
