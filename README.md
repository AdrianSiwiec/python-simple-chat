Simple server-client chat written in python3.

Usage: python3 server.py then python3 client.py "Username".

Default username is Anon. When username is taken, client automatically tries other.

Features:

- uses sockets.

- multi-threaded with no active waiting. Separate threads for sending and receiving messages both on server and client side

- can send messages to any user or broadcast to all.

- queueing of incoming messages to avoid data loss.
