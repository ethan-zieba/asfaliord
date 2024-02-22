# Asfaliord
Voice/text group chat, discord inspired, software made at La Plateforme (IT School in Marseille, France)

Uses onion-like routing and gpg encryption, as well as graphical opsec techniques.

**Python dependencies:** 
---

Server and client-side: 
`mysql, datetime, requests, http.server, random, hashlib`

Server-side only:
`mysql, datetime, uuid, http, json`

Client-side only:
`requests`

**Setup for the server:**
---

1. You will need tor, and tor-browser installed
2. Edit the torrc file to uncomment/add these two lines:  
`HiddenServiceDir /var/lib/tor/server_directory/`

    `HiddenServicePort 80 127.0.0.1:8080`
3. Go into your `/var/lib/tor/server_directory/` and get your .onion address from the hostname file
4. Anyone that wants to connect to your Asfaliord server will need this address
