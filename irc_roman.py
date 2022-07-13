import codecs
import irc_client as client


def main():
    # init
    client.authenticate()
    data = client.get_challenge(3)
    while 1:
        print("DATA: ", data)
        # Handling
        solve = codecs.decode(data, 'rot_13')
        print("Solve: ", solve)
        input("Pause")
        # End
        data = client.submit("3", solve)
        print("RESP: ", data)
        if "password" in data:
            break
        if "Bad" in data:
            print("Erreur de prog")
            break
    client.disconnect()


if __name__ == '__main__':
    main()
