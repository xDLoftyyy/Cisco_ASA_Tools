#!/usr/bin/env python

import paramiko, time

from asa_config import ip_blocks, device_username, device_pass

ip_block_1, ip_block_2, ip_block_3 = ip_blocks


def get_desc_remark():
    desc_remark = raw_input(
        "What was the description used for the change you are removing (This Needs to be accurate)? >> ")
    desc_search_term = "show access-list | inc %s" % desc_remark
    number_to_remove = input("How many lines were added below this description? >> ")
    return [desc_search_term, number_to_remove]


def connect(ip, desc_search_term, number_to_remove):
    remote_connection = paramiko.SSHClient()
    remote_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_connection.connect(
        ip,
        username=device_username,
        password=device_pass,
        look_for_keys=False,
        allow_agent=False
    )
    check_acl(remote_connection, desc_search_term, number_to_remove)


def check_acl(remote_connection, desc_search_term, number_to_remove):
    ssh_shell = remote_connection.invoke_shell()
    ssh_shell.send('enable\n')
    ssh_shell.send(device_pass + '\n')
    ssh_shell.send('terminal pager 0\n')
    shell_output = ssh_shell.recv(10000)
    ssh_shell.send(desc_search_term + '\n')
    time.sleep(1)
    shell_output = ssh_shell.recv(10000)
    filter_output = shell_output
    build_change_lines(
        remote_connection, ssh_shell, filter_output, desc_search_term, number_to_remove)


def build_and_apply(remote_connection, ssh_shell, filter_output, desc_search_term, number_to_remove):
    filter_output = filter_output.split('%s' % desc_search_term)[1]
    filter_output_eachline = filter_output.split('\n')
    filter_output_eachline = filter_output_eachline[:(number_to_remove-1)]
    time.sleep(1)
    ssh_shell.send('\n')
    ssh_shell.send('configure terminal\n')
    for each_line in reversed(filter_output_eachline):
        ssh_shell.send('no ' + each_line + '\n')
    time.sleep(1)
    ssh_shell.send('copy running-config startup-config\n')
    ssh_shell.send('\n')
    time.sleep(1)
    remote_connection.close()


def main():
    details = get_desc_remark()
    desc_search_term, number_to_remove = details

    for ip_counter in range(len(ip_block_1)):
        each_ip = ip_block_1[ip_counter]
        connect(each_ip, desc_search_term, number_to_remove)
        print(
        str(ip_counter + 1) + "\\" + str(len(ip_block_1)) +
        " ASA devices completed")
    print("Subnet 1 completed...")
    print("Moving onto subnet 2...")
    for ip_counter in range(len(ip_block_2)):
        each_ip = ip_block_2[ip_counter]
        connect(each_ip, desc_search_term, number_to_remove)
        print(
        str(ip_counter + 1) + "\\" + str(len(ip_block_2)) +
        " ASA devices completed")
    print("Subnet 2 completed...")
    print("Moving onto subnet 3...")
    for ip_counter in range(len(ip_block_3)):
        each_ip = ip_block_3[ip_counter]
        connect(each_ip, desc_search_term, number_to_remove)
        print(
        str(ip_counter + 1) + "\\" + str(len(ip_block_3)) +
        " ASA devices completed")
    print("Final subnet completed")


if __name__ == '__main__':
    main():
