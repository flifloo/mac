from subprocess import run, PIPE
from ipaddress import IPv4Address, IPv6Address
import re

# IPv4 regex
ripv4 = re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
ripv4_id = re.compile(r" *([0-9]+).* ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})")
# IPv6 regex
ripv6 = re.compile(r" *[0-9]+ +.+ ([a-f0-9]{1,4}:[a-f0-9]{1,4}:[a-f0-9]{1,4}:[a-f0-9]{1,4})::\/")
ripv6_id = re.compile(r" *([0-9]+) +.+ ([a-f0-9]{1,4}:[a-f0-9]{1,4}:[a-f0-9]{1,4}:[a-f0-9]{1,4})::\/")
# MAC regex
rmac = re.compile(r"(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9])"
                  r"{1,3}:(?:[A-F]|[0-9]){1,3}")


def get_router_ipv4(host: str, port: int, user: str, key: str) -> [IPv4Address]:
    """
    Gets IPv4 list of the router

    :param host: The SSH host of the router
    :type host: str
    :param port: The SSH port of the router
    :type port: int
    :param user: The SSH user of the router
    :type port: str
    :param key: The SSH key of the router
    :type key: str
    :return: List of IPv4 in the router
    :rtype: [IPv4Address]
    """

    out = run(["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", str(port), "/ip arp print"],
              stdout=PIPE).stdout.decode()
    return [IPv4Address(i) for i in ripv4.findall(out)]


def get_router_ipv4_id(ipv4: IPv4Address, host: str, port: int, user: str, key: str) -> int:
    """
    Get IPv4 id of the router

    :param ipv4: The IPv4 to search
    :type ipv4: IPv4Address
    :param host: The SSH host of the router
    :type host: str
    :param port: The SSH port of the router
    :type port: int
    :param user: The SSH user of the router
    :type port: str
    :param key: The SSH key of the router
    :type key: str
    :return: List of IPv4 in the router
    :rtype: int
    """

    out = run(["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", str(port), "/ip arp print"],
              stdout=PIPE).stdout.decode()
    for i in ripv4_id.findall(out):
        if i[1] == str(ipv4):
            return i[0]
    return -1


def get_router_ipv6(host: str, port: int, user: str, key: str) -> [IPv6Address]:
    """
    Gets IPv6 list of the router

    :param host: The SSH host of the router
    :type host: str
    :param port: The SSH port of the router
    :type port: int
    :param user: The SSH user of the router
    :type port: str
    :param key: The SSH key of the router
    :type key: str
    :return: List of IPv6 in the router
    :rtype: [IPv6Address]
    """

    out = run(["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", str(port),
               "/ipv6 route print"], stdout=PIPE).stdout.decode()
    return [IPv6Address(i) for i in ripv6.findall(out)]


def get_router_ipv6_id(ipv6: str, host: str, port: int, user: str, key: str) -> int:
    """
    Get IPv6 id of the router

    Return -1 if not found

    :param ipv6: The IPv6 to search
    :type ipv6: str
    :param host: The SSH host of the router
    :type host: str
    :param port: The SSH port of the router
    :type port: int
    :param user: The SSH user of the router
    :type port: str
    :param key: The SSH key of the router
    :type key: str
    :return: The id of the given IPv6
    :rtype: int
    """

    out = run(["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", str(port),
               "/ipv6 route print"], stdout=PIPE).stdout.decode()
    for i in ripv6_id.findall(out):
        if i[1] == ipv6[:-5]:
            return i[0]
    return -1


def get_router_mac(host: str, port: int, user: str, key: str) -> [str]:
    """
    Gets MAC list of the router

    :param host: The SSH host of the router
    :type host: str
    :param port: The SSH port of the router
    :type port: int
    :param user: The SSH user of the router
    :type port: str
    :param key: The SSH key of the router
    :type key: str
    :return: List of MAC in the router
    :rtype: [str]
    """

    out = run(["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", str(port), "/ip arp print"],
              stdout=PIPE).stdout.decode()
    return rmac.findall(out)
