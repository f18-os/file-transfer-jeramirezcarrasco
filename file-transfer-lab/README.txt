Tcp Tranfer file

The way this Tcp works is by first after making the socket conenction start a handshake by asking the serve
if it already has the file. If the server answer no then the client starts sending the file by parts.
To handle the proxy the client will add a header which telll the size of the packet and the server
will not stop recieving until the size is met. After the size is met then the server will send a ok.
After the Ok is receive by the client the cleint will send the next part. After the entire file is done
the Client will send a sing to tell the server that the trasnfer is complete.

There's a but that appeared at random so it was hard for me to find it but it low chances that it appears.
