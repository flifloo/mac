from ipaddress import IPv4Network, IPv4Address, AddressValueError, NetmaskValueError
from randmac import RandMac


def ipv4(prefix: str, ipl: [IPv4Address] = None, macl: [str] = None) -> [(IPv4Address, str, IPv4Address, int)]:
    """
    This function generate a list of IPs and MACs to insert.

    If a list is given, they avoid duplicated entry with list, for duplicated IP the MAC will be set to None.

    :param prefix: The IPs prefix
    :type prefix: IPv4Address
    :param ipl: A list of IPs
    :type ipl: [IPv4Address]
    :param macl: A list of MACs
    :type macl: [str]
    :return: list of tuple with IP, MAC, subnet mask and cidr
    :rtype: [(IPv4Address, str, IPv4Address, int)]
    """

    if ipl is None:
        ipl = []
    if macl is None:
        macl = []
    out = []

    # Check if prefix is valid
    try:
        ips = IPv4Network(prefix)
    except (ValueError, AddressValueError, NetmaskValueError):
        raise ValueError("Invalid prefix !")
    subnet_mask = ips.netmask
    cidr = ips.prefixlen

    # For all ip in prefix
    for ip in ips.hosts():
        mac = None
        if ip not in ipl:
            ipl.append(ip)
            mac = str(RandMac("00:00:00:00:00:00", True)).replace("'", "")
            while mac in macl:
                mac = str(RandMac("00:00:00:00:00:00", True)).replace("'", "")
            macl.append(mac)

        out.append((ip, mac, subnet_mask, cidr))
    return out
