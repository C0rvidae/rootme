import base64
import zlib

import irc_client as client


def main():
    # init
    client.authenticate()
    data = client.get_challenge(4)
    while 1:
        print(f"DATA: {data}")
        # Handling
        solve = base64.b64decode(data)
        solve = zlib.decompress(solve).decode()
        # End
        print(f"SOLVE: {solve}")
        data = client.submit("4", solve)
        print(f"RESP: {data}")
        if "password" in data:
            break
        if "Bad" in data:
            print("Erreur de prog")
            break
    client.disconnect()


if __name__ == '__main__':
    main()
