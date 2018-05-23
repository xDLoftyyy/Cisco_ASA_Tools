import getpass

def ip_builder():
    ip_prefix_1 = '10.10.10.'
    ip_prefix_2 = '8.8.8.'
    ip_prefix_3 = '192.168.1.'

    ignore_these_octets = ['7', '211']

    cidr24_last_octets = []

    for oct_count in range(1, 256):
        cidr24_last_octets.append(str(oct_count))

    for exc_count in range(len(ignore_these_octets)):
        try:
            cidr24_last_octets.remove(ignore_these_octets[exc_count])
        except ValueError:
            pass

    ip_block_1 = []
    ip_block_2 = []
    ip_block_3 = []

    for ip_count in range(len(cidr24_last_octets)):
        ip_block_1.append(ip_prefix_1 + cidr24_last_octets[ip_count])
        ip_block_2.append(ip_prefix_2 + cidr24_last_octets[ip_count])
        ip_block_3.append(ip_prefix_3 + cidr24_last_octets[ip_count])

    ## Return list of lists
    return [ip_block_1, ip_block_2, ip_block_3]

## Enter login for devices
device_username = 'Your Username'

## Taking password
device_pass = getpass.getpass("Please provide the password")

ip_blocks = ip_builder()
