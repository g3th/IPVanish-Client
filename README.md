# IPVanish-Client

## IpVanish VPN Client for Linux


![Alt text](assets/screenshot.png "Ipvanish GUI running on Kali")


### About

Written in Python with Tkinter, this app will allow you to connect to a chosen IpVanish server in most linux distributions. 


Since no linux client/app exists for IpVanish, currently, the only way to connect to a server is by downloading the ovpn configuration files, and connecting either through Network Manager or directly by setting up an OpenVPN connection.


These connections have to be created and removed (SIGINT, since there is no other way) for every server in every location which the user wishes to use. Both servers and nations are plenty, and this results in being an extremely tedious process.
Hence, this app was created, so that connecting in most linux distributions is much easier.


Since Tkinter was used, the interface is fairly basic and was only implemented to simplify the connection process (i.e. without any bells-and-whistles).

### How to Connect 

Start the app through a terminal, for instance ```python3 ipvanish.py```, and download the necessary configuration files in the ```Configs``` tab first.

Once download has completed, enter your credentials and your sudo password in the ```credentials``` tab, and store both.

Pick a city or nation by clicking on a tab, and click on ```Connect```. 

Wait a second, and a connection should be established.

You can then click ```Disconnect``` to disconnect from your current connection (via SIG. 

### How it Works

The app works by using the ```subprocess``` module to create an OpenVPN connection through terminal commands. 

As such, it requires the user to acquire superuser privileges by entering and storing the system's sudo password in the ```Credentials``` tab. The password will need to be entered every time the app starts, as it is not stored.

The systemd-resolved service is then used to set dns and various other options. Again, this requires administrative privileges.

Finally, sysctl.conf will be accessed to set/unset variable ```net.ipv6.conf.all.disable_ipv6```.

These steps have been taken in order to prevent dns requests from leaking. Visit ```dnscheck.tools``` to double-check.

### Note   

OpenVPN and systemd-resolved should be installed on your linux system.

The ```tabs``` module iterates through the system's network interfaces. Most commonly, these are named ```eth```, ```wlan``` etc...

The VPN interface should be named 'tun0'.

If problems occurr, it is likely due to these settings. Please raise an issue should this be the case.

### Installation and Requirements

**add to PATH, i.e.:**

```cp ~/Desktop/IPVanish-Client/ipvanish.py ~/Desktop/IPVanish-Client/ipvanish && rm ~/Desktop/IPVanish-Client/ipvanish.py```

```chmod +rwx ~/Desktop/IPVanish-Client/ipvanish```

```sudo mousepad ~/.bashrc (or zsh)```

**add this at the bottom of the file:**

```export PATH=$PATH:~/Desktop/IPVanish-Client/```

**now you can launch from terminal with:**

```ipvanish```

---------------------------------------------------------------------------------------------------

Requirements: 

**OpenVPN, i.e. (if not root):**

``` sudo apt-get install openvpn```

**Systemd-resolved**

```sudo apt-get install systemd-resolved```

**Image TK Module**

```sudo apt-get install python3-pil python3-pil.imagetk```

**Tk Package**

```sudo apt-get install python3-tk```

All python packages are standard library.




