#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


from __future__ import print_function 
import subprocess
import stat
import shutil

import warnings
import datetime
import time
import os
import sys



#-----------------------------------------------------------------------------#
#--------------- Exexution Functions -----------------------------------------#
#-----------------------------------------------------------------------------#

def remote_copy(file_flow, working_directory, server_USER, server_IP, server_PORT, file_server_PATH, file_local_PATH, server_KEY='', print_flag = False):

    # Recover the result
    prog_list_copy = list()
    
    prog_list_copy.append("/usr/bin/scp")
    prog_list_copy.append("-P")
    prog_list_copy.append(server_PORT)
    
    if server_KEY != '':
        prog_list_copy.append("-i")
        prog_list_copy.append(server_KEY)
    
    if file_flow == 'remote_to_local':
        prog_list_copy.append(server_USER+"@"+server_IP+":"+file_server_PATH)
        prog_list_copy.append(file_local_PATH)
    elif file_flow == 'local_to_remote':
        prog_list_copy.append(file_local_PATH)
        prog_list_copy.append(server_USER+"@"+server_IP+":"+file_server_PATH)
    else:
        sys.exit("Invalid data flow. Valid strings are: \"remote_to_local\" and \"local_to_remote\" ") 
        
    
    
    output_log = exec_and_print(prog_list_copy, '', working_directory, print_flag)
    
    return output_log


def remote_exec(prog_list, inputs_str, working_directory, server_USER, server_IP, server_PORT, server_KEY='', print_flag = False):
    
    
    
    # Execute on server
    if server_KEY != '':
        prog_list.insert(0,server_KEY)
        prog_list.insert(0,"-i")
    prog_list.insert(0,server_PORT)
    prog_list.insert(0,"-p")
    prog_list.insert(0,server_USER+"@"+server_IP)
    prog_list.insert(0,"/usr/bin/ssh")
    
    #prog_list.append("-o")
    #prog_list.append("ServerAliveInterval 60")
    
    
    output_log = exec_and_print(prog_list, inputs_str, working_directory, print_flag)
    
    return output_log


def exec_and_print(prog_list, inputs_str, working_directory, print_flag):
    
    output_log = list()
    
    if print_flag:
        for output_line in execute_program(prog_list,inputs_str, working_directory):
            print(output_line)
            output_log.append(output_line)
    else:
        for output_line in execute_program(prog_list,inputs_str, working_directory):
            output_log.append(output_line)
        
    return output_log

def execute_program(prog_list, inputs_str, working_directory):
    
    # Launch process
    launched_process = subprocess.Popen(prog_list, 
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True,
                                        cwd=working_directory)
    
    # Write imputs
    if inputs_str != '':
        launched_process.stdin.write(inputs_str)
    
    # Read output as it appears
    for stdout_line in iter(launched_process.stdout.readline, ""):
        yield stdout_line 
    launched_process.stdout.close()
    
    error_code =launched_process.stderr.readline()
    
    return_code = launched_process.wait()
    
    # If there was an error, rise an error in execution
    if return_code:
        val = ' '.join(prog_list)
        print('-------------------------------------------------------------------------------------------------------------------')
        print('------------------------------------------------ ERROR ------------------------------------------------------------')
        print('-------------------------------------------------------------------------------------------------------------------')
        print("Return Code:\n" + str(return_code) + "\n\nError Code:\n" +error_code+"\n\nIssued Line:\n"+val+"\n\nIssued Std_Input:\n"+inputs_str)
        print('-------------------------------------------------------------------------------------------------------------------')
        raise subprocess.CalledProcessError(return_code, prog_list)
    
    return 