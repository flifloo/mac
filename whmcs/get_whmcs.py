from pymysql import Connect
from ipaddress import IPv4Address


def get_whmcs_ipv4(db: Connect) -> [IPv4Address]:
    """
    Get all IPs of WHMCS

    :param db: The database connection of WHMCS
    :type db: pymysql.Connect
    :return: The list of WHMCS IP
    :rtype: [IPv4Address]
    """

    cursor = db.cursor()
    cursor.execute("SELECT ip FROM mg_proxmox_addon_ip")
    ips = [IPv4Address(i[0]) for i in cursor.fetchall()]
    cursor.close()
    return ips


def get_whmcs_mac(db: Connect) -> [str]:
    """
    Get all MACs of WHMCS

    :param db: The database connection of WHMCS
    :type db: pymysql.Connect
    :return: The list of WHMCS MAC
    :rtype: [str]
    """

    cursor = db.cursor()
    cursor.execute("SELECT mac_address FROM mg_proxmox_addon_ip")
    macs = [i[0] for i in cursor.fetchall()]
    cursor.close()
    return macs
