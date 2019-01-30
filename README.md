# Coding challenge

This project includes a server and a client for achieving the task of resolving arithmetical operations.
Server and client comunicates each other with sockets.

# How to use

## server.py
- Receives math operations, one per line, and return results, one per line.  
- Operations file should content a list of math operations, one per line.
- Every line have to end with end of line character (\n)
- Only +, -, *, / operators are allowed.
- In order to avoid propagation errors, results are calculated float divisions (instead of integer division)


Run server:
```console
>>> python server.py
```

## client.py
In other terminal run client. If destination file doesn't exist it creates a new one:
```console
>>> python client [origin_file] [destination_file]
```

Example
```console
>>> python client.py myoperations.txt myresults.txt
```

If not parameters are specified it uses operations.txt and results.txt as source and destination files as default, respectively.
```console
>>> python client.py
```
is equivalent to:
```console
>>> python client.py operations.txt results.txt
```

### Requirements:
Python 2.7
No external libraries or dependencies
