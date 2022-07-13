import base64
import irc_client as client


def main():
    # init
    client.authenticate()
    while 1:
        data = client.get_challenge(2)
        print("DATA: ", data)
        if "password" in data:
            break
        # Handling
        solve = base64.b64decode(data).decode()
        print("Solve: ", solve)
        input("Pause")
        # End
        client.submit("2", solve)
    client.disconnect()


if __name__ == '__main__':
    main()
