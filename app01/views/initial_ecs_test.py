from django.shortcuts import render
import paramiko
import threading
import sys, os

"""
hostlist is the host you wanna deploy,after finishing setting, run python demo_connect_test.py
attention: ip & passwd

"""
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def connect_to_remote_host(hostip, username, password):
    client = paramiko.client.SSHClient(
    )  # A high-level representation of a session with an SSH server
    client.load_system_host_keys()  # 读known hosts文件里的public key，没有再说
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())  # 或者接受用WarningPolicy()
    client.connect(hostname=hostip, username=username, password=password)
    return client


def excute_command(client, command):
    try:
        stdin, stdout, stderr = client.exec_command(command)

    except:
        err = stderr.read().decode()
        client.close()
        exit(1)
        return err
    else:
        standout = stdout.read().decode()
        return standout



def work_loop(y_host, y_user, y_passwd, host, t_user, t_passwd):
    # upload initial.sh,next.sh,python3.6 package
    client = connect_to_remote_host(hostip=y_host,
                                    username=y_user,
                                    password=y_passwd)

    excute_command(
        client=client,
        command=
        'cat /root/copy_jdk_shell/mark.txt > /root/copy_jdk_shell/copy_initial_shell.log 2>&1'
        )  # yunwei machine log
    client.close()
    # excute initial.sh
    client = connect_to_remote_host(hostip=host,
                                    username=t_user,
                                    password=t_passwd)
    excute_command(client,
                   command=
                   'cat /root/mark.txt > /root/initial.log 2>&1')  # target machine log
    client.close()


def yunwei_log_catch(y_host, y_user, y_passwd):
    client = connect_to_remote_host(hostip=y_host,
                                    username=y_user,
                                    password=y_passwd)
    yunwei_log = excute_command(client,
                                command=
                                'cat /root/copy_jdk_shell/copy_initial_shell.log ')
    client.close()
    return yunwei_log



def target_machine_log_catch(host, t_user, t_passwd, log):
    client = connect_to_remote_host(hostip=host,
                                    username=t_user,
                                    password=t_passwd)
    output = excute_command(client,
                            command=
                            'cat /root/initial.log')
    target_machine_log = log + output
    client.close()
    return target_machine_log



def initial(request):
    if request.method == 'GET':
        return render(request, 'initial-ecs.html')
    else:
        ip_address = request.POST.get('ip_address')
        hostlist = ip_address.split()
        print(hostlist)
        t_user = "root"
        t_passwd = "jacob"
        y_host = "192.168.1.253"
        y_user = "root"
        y_passwd = "jacob"
        host_num = len(hostlist)
        for i in range(host_num):
            t = threading.Thread(name='process on {}'.format(hostlist[i]),
                                target=work_loop,
                                args=(y_host, y_user, y_passwd, hostlist[i],
                                        t_user, t_passwd))
            t.start()
            t.join()

    yunwei_log = yunwei_log_catch(y_host, y_user, y_passwd)
    target_machine_log = ""
    for i in range(host_num):
        target_machine_log = target_machine_log_catch(hostlist[i], t_user, t_passwd,target_machine_log)

    return render(request, 'initial-ecs.html', {'yunwei_log':yunwei_log, 'target_machine_log':target_machine_log})
