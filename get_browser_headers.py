from argparse import Namespace
from socket import AF_INET, SOCK_STREAM, socket

import yaml

# output as json or plaint text, print to file or stdout


def to_structured(data: str) -> dict[str, str]:
    structured = {}
    for line in data.strip().split("\r\n"):
        if line.startswith("GET") or line.startswith("Host"):
            continue
        if not line:
            continue
        key, value = line.split(": ", 1)
        structured[key] = value
    return structured


def main(args: Namespace):
    print(f"Listening on http://{args.host}:{args.port}", end="\n\n")
    with socket(AF_INET, SOCK_STREAM) as soc, open(args.output, "w") as fd:
        soc.bind((args.host, args.port))
        soc.listen()
        conn, _ = soc.accept()
        with conn:
            data = conn.recv(1024)
            decoded = data.decode()
            if "GET / " in decoded:
                structured = to_structured(decoded)
                yaml.dump(structured, fd, default_flow_style=False, sort_keys=False)

                conn.send(b"HTTP/1.1 200 OK\n")
                conn.send(b"Content-Type: text/html\n")
                conn.send(b"\n")
                conn.send(b"<html><body><pre>")
                conn.send(data)
                conn.send(b"</pre></body></html>")
                conn.close()


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-o", "--output", default="config/headers.yaml")
    parser.add_argument("-p", "--port", type=int, default=65432)
    args = parser.parse_args()

    main(args)
