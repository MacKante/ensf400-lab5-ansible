import ansible_runner
import re

# Load Inventory
def load_inventory():
    print('Retrieving invetory...')

    response, error = ansible_runner.interface.get_inventory(
        action='list',
        inventories=['./hosts.yml'],
        response_format='json',
        quiet=True
    )

    # Retrieve IP addresses of all hosts
    all_hosts = list(response['_meta']['hostvars'].keys())
    ip_addresses = {}
    for host in all_hosts:
        ip_address = retrieve_ip(host)
        ip_addresses[host] = ip_address

    # Keys to exclude
    keys_to_exclude = ['_meta', 'all']

    # Duplicate response dict with only the groups
    groups = {key: response[key] for key in response if key not in keys_to_exclude}
    
    # Print the groups and the info of each host
    print('\n------------------------------------------------------------------------')
    print('Printing Final Results')
    for group, hosts in groups.items():
        # Retrieve hosts in group
        host_list = hosts['hosts']

        print(f'Group: {group}...')
        print('Hosts:')

        # Print host name and IP adress
        for host in host_list:
            ip_address = ip_addresses[host]
            print(f'    {host}:')
            print(f'        IP Address: {ip_address}')

        print()

def retrieve_ip(target_host):
    # play the ansible playbook
    response, error, code = ansible_runner.interface.run_command(
        executable_cmd=f"ansible-playbook retrieve_ip.yml -e 'target_host={target_host}'"
    )

    # Define the regular expression pattern to match the IP address
    pattern = r'"msg": "(\d+\.\d+\.\d+\.\d+)"'

    # Search for the IP address in the output
    match = re.search(pattern, response)

    # If a match is found, extract the IP address
    if match:
        ip_address = match.group(1)
        return ip_address
    else:
        return "Trouble retrieving IP address"

load_inventory()