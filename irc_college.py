import math

import irc_client as client


def main():
    client.authenticate()
    data = client.get_challenge(1)
    # input("pause")
    print("DATA: ", data)
    reps = data.split('/')
    rep = [int(r.strip()) for r in reps]
    print("Numbers: ", rep)
    solve = math.sqrt(rep[0])
    solve *= rep[1]
    solve = round(solve, 2)
    print("Answer: ", solve)
    data = client.submit("1", str(solve))
    # input("Pause main")
    data = client.get_challenge(1)
    client.disconnect()


if __name__ == '__main__':
    main()
