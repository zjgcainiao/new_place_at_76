
# utility function to anonymize ip address
def anonymize_ip(ip):
    """
    Anonymizes the given IP address by replacing the last octet with '0'.

    Args:
        ip (str): The IP address to be anonymized.

    Returns:
        str: The anonymized IP address.

    """
    if ip:
        parts = ip.split('.')
        if len(parts) == 4:  # For IPv4
            parts[3] = '0'
        return '.'.join(parts)
    return ip
