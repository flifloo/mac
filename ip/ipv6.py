def link_local(mac: str) -> str:
    """
    Convert MAC to IPv6 Link-local address

    :param mac: MAC address
    :type mac: str
    :return: IPv6 Link-local address
    :rtype: str
    """
    # only accept MACs separated by a colon
    parts = mac.split(":")

    # modify parts to match IPv6 value
    parts.insert(3, "ff")
    parts.insert(4, "fe")
    parts[0] = "%x" % (int(parts[0], 16) ^ 2)

    # format output
    ipv6_parts = []
    for i in range(0, len(parts), 2):
        ipv6_parts.append("".join(parts[i:i+2]))
    ipv6 = "fe80::%s" % (":".join(ipv6_parts))
    return ipv6
