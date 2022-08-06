# IPVanish-Client

### IPVanish simple GUI for Linux/Debian

-----------------------------------------------------------------------

![Alt text](assets/screenshot.png "Ipvanish GUI running on Kali")

Connecting to IPVanish is normally quite annoying in Debian/Linux. It requires manually adding a connection, loading the file, and entering the password. This is for **every single server** you want to connect to.

This GUI somewhat simplifies the process. 

By launching the GUI you will have the option to download the ovpn configurations, entering valid credentials, connecting and disconnecting to a server of your choice.

It is up to you to enter valid credentials, as they are not checked by using authentication with an api endpoint.

Unfortunately the credentials is a text file stored in '/configs'/. 

That might change in the future. I see no real problem, unless you are on a shared-terminal or in an office. 

I don't have that problem: I share nothing and live in a cave, and I wrote this for myself after all.

----------------------------------------------------------------------------------------------------
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

``` sudo -i ```

``` apt-get install openvpn```

**Works through nmcli, so Network Manager must be enabled, i.e.:**

```systemctl start NetworkManager```
```systemctl enable NetworkManager```

All packages are standard library.

Passwords are not outputted to terminal thanks to ```stdout=subprocess.DEVNULL``` and redirecting output to the linux toilet (they might be stored elsewhere in memory).

---------------------------------------------------------------------------------------------------

Where we are:

Current version is fully functional and code is a bit more structured. There is still quite a lot to do:

- Fix the generic North America, Europe and South America choices
- ~~Disconnect and delete connection~~			(26/07/22)
- ~~Update buttons and label~~					(26/07/22)
- ~~Add Credentials tab~~						(26/07/22)
- ~~Add Settings tab~~							(29/07/22)
- ~~Add Configuration Downloading (Settings)~~	(29/07/22)
- General GUI style



