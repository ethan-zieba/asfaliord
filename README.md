# Asfaliord
Voice/text group chat, discord inspired, software made at La Plateforme (IT School in Marseille, France)

Uses onion routing and gpg encryption as well as graphical opsec techniques.

**Python dependencies:** 
---

Server and client-side: 
`mysql, datetime, requests, http.server, random, hashlib`

Server-side only:
`mysql, datetime, uuid, http, json`

Client-side only:
`requests`

**Setup for the server on Debian-based distros:**
---

(Be aware that there might be some safer ways to go about hosting the server, we are not responsible for the security of your server. We are learning everyday to make our security and opsec better)

1. Clone the repo
2. Install tor ( https://community.torproject.org/onion-services/setup/ )
3. With a sudoer user edit the torrc file to uncomment/add these two lines: 
`HiddenServiceDir /var/lib/tor/server_directory/`
`HiddenServicePort 80 127.0.0.1:8080`
4. As root go into `/var/lib/tor` and create the `server_directory` directory (you can name it differently as long as you modify your `torrc` file accordingly)
5. Change the owner of the `server_directory` to `debian-tor`
6. Make the user that is gonna run tor a part of the `debian-tor` group
7. Switch back to the user running tor and restart tor with : `sudo systemctl restart tor`
8. Go into your `/var/lib/tor/server_directory/` and get your .onion address from the hostname file

If you encounter any problems checking out /var/lib/syslog might help
