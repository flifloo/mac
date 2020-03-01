from ipaddress import IPv4Address
from router.get_router import get_router_ipv4_id, get_router_ipv6_id
from subprocess import run


def remove_router_ipv4(remove: [(IPv4Address, str, IPv4Address, int)], host: str, port: int, user: str,
                       key: str, debug: bool = False, verbose: bool = False):
    """
    This function remove IPv6 on the router

    :param remove: The list of IPs, MACs to remove
    :type remove: [(IPv4Address, str, IPv4Address, int)]
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
    """

    print("Start remove IPv4 on router")
    for i in remove:
        id = get_router_ipv4_id(i[0], host, port, user, key)
        if id != -1:
            cmd = ["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", str(port),
                   f"/ip arp remove {id}"]
            if not debug:
                run(cmd)
            if debug or verbose:
                print(cmd)
        elif debug or verbose:
            print(f"IPv4:{i[0]} not found")
    print("Remove IPv4 on router done")


def remove_router_ipv6(remove: [(IPv4Address, str, IPv4Address, int)], ipv6: str, host: str, port: int, user: str,
                       key: str, debug: bool = False, verbose: bool = False):
    """
    This function remove IPv6 on the router

    :param remove: The list of IPs, MACs to remove
    :type remove: [(IPv4Address, str, IPv4Address, int)]
    :param ipv6: The IPV6 template
    :type ipv6: str
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
    """

    print("Start remove IPv6 on router")
    for i in remove:
        ip = ipv6.format(str(i[0]).split(".")[-1])
        id = get_router_ipv6_id(ip, host, port, user, key)
        if id != -1:
            cmd = ["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", str(port),
                   f"/ipv6 route remove {id}"]
            if not debug:
                run(cmd)
            if debug or verbose:
                print(cmd)
        elif debug or verbose:
            print(f"IPv6:{ip} not found")
    print("Remove IPv6 on router done")
