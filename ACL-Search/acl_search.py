#!/usr/bin/env python

import paramiko, time, email_report

from asa_config import ip_blocks, device_username, device_pass

ip_block_1, ip_block_2, ip_block_3 = ip_blocks


def get_search_criteria():
    how_many = input("How many Terms do you wish to search for ? >> ")
    search_terms = []
    for count in range(how_many):
        term = raw_input("Please provide search term %s >> " % str(count+1))
        search_terms.append(term)
    return search_terms


def connect(ip):
    remote_connection = paramiko.SSHClient()
    remote_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_connection.connect(
        ip,
        username=device_username,
        password=device_pass,
        look_for_keys=False,
        allow_agent=False
    )
    return remote_connection


def search_acl(remote_connection, search_terms):
    ssh_shell = remote_connection.invoke_shell()
    ssh_shell.send('enable\n')
    ssh_shell.send(device_pass + '\n')
    ssh_shell.send('terminal pager 0\n')
    shell_output = ssh_shell.recv(10000)
    results = []
    for each_term in search_terms:
        ssh_shell.send("show access-list | inc %s\n" % each_term)
        time.sleep(1)
        shell_output = ssh_shell.recv(10000)
        output_trimmed = shell_output.split('show access-list | inc %s' % each_term)[1]
        results.append(output_trimmed)
    return results


def main():
    search_terms = get_search_criteria()
    file1 = open("Subnet-1-Results.txt", "a+")
    for each_ip in ip_block_1:
        remote_connection = connect(each_ip)
        results = search_acl(remote_connection, search_terms)
        file1.write(" \n")
        file1.write(each_ip + " \n")
        for result in results:
            file1.write(result + " \n")
        file1.write("-----------------------------------------------------")
    file1.close()
    print("Subnet 1 complete\n")
    file2 = open("Subnet-2-Results.txt", "a+")
    for each_ip in ip_block_2:
        remote_connection = connect(each_ip)
        results = search_acl(remote_connection, search_terms)
        file2.write(" \n")
        file2.write(each_ip + " \n")
        for result in results:
            file2.write(result + " \n")
        file2.write("-----------------------------------------------------")
    file2.close()
    print("Subnet 2 complete\n")
    file3 = open("Subnet-3-Results.txt", "a+")
    for each_ip in ip_block_3:
        remote_connection = connect(each_ip)
        results = search_acl(remote_connection, search_terms)
        file3.write(" \n")
        file3.write(each_ip + " \n")
        for result in results:
            file3.write(result + " \n")
        file3.write("-----------------------------------------------------")
    file3.close()
    print("Subnet 3 complete\n")
    email = raw_input("Search Complete would you like the results emailed to you ? y/n >> ")
    if email == ("y"):
        email_report.build_message()


if __name__ == '__main__':
    main()


