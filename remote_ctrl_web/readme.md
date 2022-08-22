To serve the website on local network, install python and then:
python -m http.server --bind 0.0.0.0

Website is accessible on localhost:8000 or 192.168.X.X:8000   (with X.X the IP address on local network of the computer serving the website)

http://localhost:8000/remote.html

To find the IP on the club robot network, go to DHCP lease in 192.168.42.1

(On Windows without path) :
"C:\Program Files\Python310\python.exe" -m http.server 8888 --bind 0.0.0.0