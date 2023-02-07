# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import subprocess
import sys
import psycopg2

node_obj_nm = []
groups = '"all,bmc"'
chain_setup = '"runcmd=bmcsetup"'
os_name = sys.argv[1]
chain_os = f"osimage={os_name}"


def get_node_obj():
    command = "lsdef"
    node_objs = subprocess.run([f'{command}'], shell=True, capture_output = True)
    print(node_objs.stdout)
    temp = str(node_objs.stdout).split('\n')
    for i in range(0, len(temp) - 1):
        node_obj_nm.append(temp[i].split(' ')[0])
    print(node_obj_nm)

    update_node_obj_nm()


def update_node_obj_nm():
    # Establish a connection with omniadb
    conn = psycopg2.connect(
        database="omniadb",
        user='postgres',
        host='localhost',
        port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    sql = '''select serial from cluster.nodeinfo'''
    cursor.execute(sql)
    serial_output = cursor.fetchall()

    for i in range(0, len(serial_output)):
        serial_output[i] = str(serial_output[i][0]).lower()
    for i in (0, len(serial_output) - 1):
        serial_output[i] = serial_output[i].upper()
        sql = '''select node from cluster.nodeinfo where serial='{serial_key}' '''.format(serial_key=serial_output[i])
        cursor.execute(sql)
        node_name = cursor.fetchone()
        sql = '''select admin_ip from cluster.nodeinfo where serial='{serial_key}' '''.format(
            serial_key=serial_output[i])
        cursor.execute(sql)
        admin_ip = cursor.fetchone()
        command = f"chdef {node_name[0]} -p ip={admin_ip[0]} groups={groups} chain={chain_setup},{chain_os}"
        node_objs = subprocess.run([f'{command}'], shell=True)

    cursor.close()
    conn.close()

get_node_obj()
