To serve the website on local network, install python and then:
python -m http.server --bind 0.0.0.0

Website is accessible on localhost:8000 or 192.168.X.X:8000   (with X.X the IP address on local network of the computer serving the website)

(On Windows without path) :
"C:\Program Files\Python310\python.exe" -m http.server 8888 --bind 0.0.0.0