#!/usr/bin/env python

import paramiko, time

from asa_config import ip_blocks, device_username, device_pass

ip_block_1, ip_block_2, ip_block_3 = ip_blocks


def get_filter():
    inc_filter = raw_input(
    "Please provide the access-list line you wish to add above >> ")
    inc_filter_command = "show access-list | inc %s" % inc_filter
    return inc_filter_command


def get_desc_remark():
    change_desc = raw_input(
    "Please provide a short description of the purpose of your change >> ")
    change_desc_line = (" remark --- %s") % change_desc
    return change_desc_line


def get_config_lines():
    config_lines = []
    how_many_config = input("How many lines of config do you wish to add ? >> ")
    for i in range(how_many_config):
        each_line = raw_input("Please provide each line of configuration individually."
                              " Provide them in the order you wish them to appear starting from the top >> ")
        config_lines.append(each_line)
    return config_lines


def connect(ip, inc_filter_command, change_desc_line, config_lines):
    remote_connection = paramiko.SSHClient()
    remote_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_connection.connect(
        ip,
        username=device_username,
        password=device_pass,
        look_for_keys=False,
        allow_agent=False
    )
    check_acl(
    remote_connection, inc_filter_command, change_desc_line, config_lines)


def check_acl(
remote_connection, inc_filter_command, change_desc_line, config_lines):
    ssh_shell = remote_connection.invoke_shell()
    ssh_shell.send('enable\n')
    ssh_shell.send(device_pass + '\n')
    ssh_shell.send('terminal pager 0\n')
    shell_output = ssh_shell.recv(10000)
    ssh_shell.send(inc_filter_command + '\n')
    time.sleep(1)
    shell_output = ssh_shell.recv(10000)
    filter_output = shell_output
    build_change_lines(
    remote_connection, ssh_shell, filter_output, inc_filter_command,
    change_desc_line, config_lines)


def build_change_lines(
remote_connection, ssh_shell, filter_output, inc_filter_command,
change_desc_line, config_lines):
    words_for_format = []
    device_and_interface = []
    line_numbers = []
    full_config_lines = []
    remark_line = ' remark > '
    filter_output = filter_output.split('%s' % inc_filter_command)[1]
    filter_output_each_line = filter_output.split('\n')
    for each_line in filter_output_each_line:
        each_word = each_line.split()
        words_for_format.append(each_word)
    words_for_format.remove([])
    words_for_format.pop(-1)
    for words in words_for_format:
        line_numbers.append(words[3])
        device_and_interface.append(words[0:3])
    for counter in range(len(device_and_interface)):
        device_and_interface_joined = ' '.join(device_and_interface[counter])
        full_remark_line = (
        device_and_interface_joined + ' ' + line_numbers[counter] + remark_line)
        for i in range(len(config_lines)):
            full_config_line = (
            device_and_interface_joined + ' ' + line_numbers[counter] + ' '
            + config_lines[i])
            full_config_lines.append(full_config_line)
        full_desc_line = (
        device_and_interface_joined + ' ' + line_numbers[counter] + ' ' +
        change_desc_line)
        apply_config(remote_connection, ssh_shell, full_desc_line,
        full_config_lines, full_remark_line)


def apply_config(
remote_connection, ssh_shell, full_desc_line, full_config_lines,
full_remark_line):
    time.sleep(1)
    ssh_shell.send('\n')
    ssh_shell.send('configure terminal\n')
    ssh_shell.send(full_remark_line + '\n')
    for each_config in reversed(full_config_lines):
        ssh_shell.send(each_config + '\n')
        time.sleep(1)
    ssh_shell.send(full_desc_line + '\n')
    time.sleep(1)
    ssh_shell.send('copy running-config startup-config\n')
    ssh_shell.send('\n')
    time.sleep(1)
    remote_connection.close()


def main():
    inc_filter_command = get_filter()
    change_desc_line = get_desc_remark()
    config_lines = get_config_lines()
    for ip_counter in range(len(ip_block_1)):
        each_ip = ip_block_1[ip_counter]
        connect(each_ip, inc_filter_command, change_desc_line, config_lines)
        print(
        str(ip_counter + 1) + "\\" + str(len(ip_block_1)) +
        " ASA devices completed")
    print("Subnet 1 completed...")
    print("Moving onto subnet 2...")
    for ip_counter in range(len(ip_block_2)):
        each_ip = ip_block_2[ip_counter]
        connect(each_ip, inc_filter_command, change_desc_line, config_lines)
        print(
        str(ip_counter + 1) + "\\" + str(len(ip_block_2)) +
        " ASA devices completed")
    print("Subnet 2 completed...")
    print("Moving onto subnet 3...")
    for ip_counter in range(len(ip_block_3)):
        each_ip = ip_block_3[ip_counter]
        connect(each_ip, inc_filter_command, change_desc_line, config_lines)
        print(
        str(ip_counter + 1) + "\\" + str(len(ip_block_3)) +
        " ASA devices completed")
    print("Final subnet completed")


if __name__ == '__main__':
    main():
