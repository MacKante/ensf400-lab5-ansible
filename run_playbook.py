import ansible_runner
import urllib.request
import subprocess


# Ensure setup
subprocess.run("docker compose up -d", shell=True)
subprocess.run("export ANSIBLE_CONFIG=$(pwd)/ansible.cfg", shell=True)

# Retrieve ssh key
with open("./secrets/id_rsa", "r") as f:
    ssh_key = f.read()

# Run the playbook
runner = ansible_runner.run(private_data_dir=".", playbook='./hello.yml', inventory='./hosts.yml', ssh_key=ssh_key)

expected_messages = ["Hello World from managedhost-app-1 !", "Hello World from managedhost-app-2 !", "Hello World from managedhost-app-3 !"]
actual_messages = []

print("\nVerifying servers...")
for i in range(6):
    response = urllib.request.urlopen("http://0.0.0.0")
    msg = response.read().decode("utf-8")
    actual_messages.append(msg)
    print(msg)

if (actual_messages[:3] == expected_messages) and (actual_messages[3:] == expected_messages):
    print("\nExpected output from servers is correct...")
else:
    print("\nUnexpected output from servers")
    print(actual_messages)