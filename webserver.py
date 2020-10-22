# Source: https://ruslanspivak.com/lsbaws-part1/
import socket
import sys

def receive(client_connection):
    request_data = b''
    while True:
      new_data = client_connection.recv(4098)
      if (len(new_data) == 0):
        # client disconnected
        return None, None
      request_data += new_data
      if b'\r\n\r\n' in request_data:
        break

    parts = request_data.split(b'\r\n\r\n', 1)
    header = parts[0]
    body = parts[1]

    if b'Content-Length' in header:
      headers = header.split(b'\r\n')
      for h in headers:
        if h.startswith(b'Content-Length'):
          blen = int(h.split(b' ')[1]);
          break
    else:
        blen = 0

    while len(body) < blen:
      body += client_connection.recv(4098)

    print(header.decode('utf-8', 'replace'), flush=True)
    print('')
    print(body.decode('utf-8', 'replace'), flush=True)

    return header, body


#'192.168.0.100'
HOST, PORT, PATH = sys.argv[1], int(sys.argv[2]), sys.argv[3]

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT} ...')
while True:
    client_connection, client_address = listen_socket.accept()
    header, body = receive(client_connection)
    if header is None or body is None:
        client_connection.close()
        continue

    #Rejects Firefox browser users
    elif (b'Firefox' in header):
        http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

<html>
<head>
    <meta charset=“utf-8”>
    <title>Browser Error!</title>
</head>
<body>
<h1><font = color = "red">Browser Error:</font></h1>
<p><font = color = "red">It has been detected that the Firefox browser is in use.</font></p>
<p><b><font = color = "blue">Please switch browser to connect to this page!</font></b></p>
</body>
</html>

"""
        http_response = http_response.replace('\n', '\r\n').encode('UTF-8')

    #Opens a .html file
    elif (b'html' in header.split(b' ')[1]):
        http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

"""
        http_response = http_response.replace('\n', '\r\n').encode('UTF-8')
        try:
            with open(PATH + header.split(b' ')[1].decode(), 'rb') as fh:
                http_response += fh.read()
        #If .html file not in directory 404 response sent
        except:
            http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

<html>
<head>
    <meta charset=“utf-8”>
    <title>404 Error!</title>
</head>
<body>
<b><font = color = "red">File not found! (404 error)</font></b>
</body>
</html>

"""
            http_response = http_response.replace('\n', '\r\n').encode('UTF-8')

    #Opens a .jpg file
    elif (b'jpg' in header.split(b' ')[1]):
        http_response = """\
HTTP/1.1 200 OK
Content-Type: image/jpeg
Connection: close

"""
        http_response = http_response.replace('\n', '\r\n').encode('UTF-8')
        try:
            with open(PATH + header.split(b' ')[1].decode(), 'rb') as fh:
                http_response += fh.read()
        #If .jpg file not in directory 404 response sent
        except:
            http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

<html>
<head>
    <meta charset=“utf-8”>
    <title>404 Error!</title>
</head>
<body>
<b><font = color = "red">File not found! (404 error)</font></b>
</body>
</html>

"""
            http_response = http_response.replace('\n', '\r\n').encode('UTF-8')

    #Opens a .png file
    elif (b'png' in header.split(b' ')[1]):
        http_response = """\
HTTP/1.1 200 OK
Content-Type: image/png
Connection: close

"""
        http_response = http_response.replace('\n', '\r\n').encode('UTF-8')
        try:
            with open(PATH + header.split(b' ')[1].decode(), 'rb') as fh:
                http_response += fh.read()
        #If .png file not in directory 404 response sent
        except:
            http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

<html>
<head>
    <meta charset=“utf-8”>
    <title>404 Error!</title>
</head>
<body>
<b><font = color = "red">File not found! (404 error)</font></b>
</body>
</html>

"""
            http_response = http_response.replace('\n', '\r\n').encode('UTF-8')

    #If file cannot be found sends a 404 response
    else:
        http_response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

<html>
<head>
    <meta charset=“utf-8”>
    <title>404 Error!</title>
</head>
<body>
<b><font = color = "red">File not found! (404 error)</font></b>
</body>
</html>

"""
        http_response = http_response.replace('\n', '\r\n').encode('UTF-8')

    client_connection.sendall(http_response)
    client_connection.close()
