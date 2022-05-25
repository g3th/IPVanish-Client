# IPVanish-Client

### IPVanish simple GUI for Linux/Debian

Connecting to IPVanish is normally quite annoying in Debian/Linux. It requires manually adding a connection, loading the file, and entering the password. This is for **every single server** you want to connect to.

This GUI somewhat simplifies the process. 

Launch the script and it will do various things:

```
- Check if you have a '/Config/' folder where Ipvanish open-vpn configuration files are stored.
- Check if that folder is populated
- If you have no config files it will download them for you, after having created the appropriate folder.
- Will prompt for user-name and password, with 'echo-off'. 
```

The GUI is then launched, and a connection is chosen. In the current version, it is only possible to select 'Cities'.

Unfortunately the credentials is a text file stored in '/configs'/. 

That might change in the future. I see no real problem, unless you are on a shared-terminal or in an office. 

I don't have that problem, I share nothing and live in a cave, and I wrote this for myself after all.


----------------------------------------------------------------------------------------------------


Requirements: None, all packages are standard library.

Works through nmcli, so Network Manager must be enabled, i.e.:

```systemctl start NetworkManager```
```systemctl enable NetworkManager```

Works with 'subprocess' but risk of injection has been minimized with 'Shlex' parser and 'Shell=False'.


