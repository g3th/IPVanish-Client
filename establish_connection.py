import signal
import os
import subprocess
import threading
from pathlib import Path
from subprocess import PIPE


class EstablishConnection:
    def __init__(self, sudo_pass):
        self.network_interfaces_list = os.listdir("/sys/class/net")
        self.default_gateway = '192.168.0.1'
        self.ipvanish_dns = ['198.18.0.1', '198.18.0.2']
        self.sudo_password = sudo_pass
        self.configuration_files_path = str(Path(__file__).parent) + "/configs"
        self.pid = None

    def open_vpn_connection(self):
        connect = ['sudo', '-S', 'openvpn', '--config', self.configuration_files_path + "/conn.ovpn"]
        disable_ipv6 = ['sudo', '-S', 'sysctl', 'net.ipv6.conf.all.disable_ipv6=1']
        run_ipv6 = subprocess.Popen(disable_ipv6, shell=False, stdin=PIPE, encoding='utf-8')
        run = subprocess.Popen(connect, shell=False, stdin=PIPE, encoding='utf-8')
        with open("pid", 'w') as process_id:
            process_id.write(str(run.pid))
        process_id.close()
        run_ipv6.communicate(input=self.sudo_password)
        run.communicate(input=self.sudo_password)

    def set_options(self):
        for interface in self.network_interfaces_list:
            commands_as_list_of_lists = [['sudo', '-S', 'resolvectl', 'default-route', interface, 'false'],
                                         ['sudo', '-S', 'resolvectl', 'llmnr', interface, 'false'],
                                         ['sudo', '-S', 'resolvectl', 'mdns', interface, 'false'],
                                         ['sudo', '-S', 'resolvectl', 'dns', interface, self.ipvanish_dns[0],
                                          self.ipvanish_dns[1]]]
            for command in commands_as_list_of_lists:
                if "tun0" not in interface and interface != "lo":
                    self.launch_command(command)
        tunnel_options = [['sudo', '-S', 'resolvectl', 'dns', 'tun0', self.ipvanish_dns[0], self.ipvanish_dns[1]],
                          ['sudo', '-S', 'resolvectl', 'default-route', 'tun0', 'true']]
        for t_opt in tunnel_options:
            self.launch_command(t_opt)

    def start_connection(self):
        threading.Thread(target=self.open_vpn_connection, args=()).start()

    def launch_command(self, command):
        subprocess.Popen(command, shell=False,
                         stdin=PIPE, encoding='utf-8').communicate(input=self.sudo_password)

    def disconnect(self):
        pid = open("pid", 'r').readline()
        os.kill(int(pid), signal.SIGINT)
        os.remove("pid")
        for interface in self.network_interfaces_list:
            commands_as_list_of_lists = [['sudo', '-S', 'sysctl', 'net.ipv6.conf.all.disable_ipv6=0'],
                                         ['sudo', '-S', 'resolvectl', 'default-route', interface, 'true'],
                                         ['sudo', '-S', 'resolvectl', 'dns', interface, self.default_gateway]]
            for command in commands_as_list_of_lists:
                self.launch_command(command)
# sudo sysctl net.ipv6.conf.all.disable_ipv6=1
# connect ovpn
# options
# Global
#          Protocols: +LLMNR +mDNS -DNSOverTLS DNSSEC=no/unsupported
#   resolv.conf mode: foreign
#
# Link 2 (eth0)
#     Current Scopes: none
#          Protocols: +DefaultRoute +LLMNR +mDNS -DNSOverTLS DNSSEC=no/unsupported
#        DNS Servers: 192.168.0.1
#
# Link 12 (wlan0)
#     Current Scopes: DNS LLMNR/IPv4 mDNS/IPv4
#          Protocols: +DefaultRoute +LLMNR +mDNS -DNSOverTLS DNSSEC=no/unsupported
# Current DNS Server: 198.18.0.1
#        DNS Servers: 198.18.0.1 198.18.0.2
#
# Link 16 (tun0)
#     Current Scopes: DNS LLMNR/IPv4 mDNS/IPv4
#          Protocols: +DefaultRoute +LLMNR +mDNS -DNSOverTLS DNSSEC=no/unsupported
# Current DNS Server: 198.18.0.1
#        DNS Servers: 198.18.0.1 198.18.0.2
