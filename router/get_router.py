from subprocess import run, PIPE
from ipaddress import IPv4Address
import re

rip = re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")  # IP regex
rmac = re.compile(r"(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9]){1,3}:(?:[A-F]|[0-9])"
                  r"{1,3}:(?:[A-F]|[0-9]){1,3}")  # MAC regex


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
    return [IPv4Address(i) for i in rip.findall(out)]


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

    out = run(["ssh", "-i", key, "-o", "StrictHostKeyChecking no", f"{user}@{host}", "-p", port, "/ip arp print"],
              stdout=PIPE).stdout.decode()
    return rmac.findall(out)
