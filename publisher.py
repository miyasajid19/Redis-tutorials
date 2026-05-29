"""Simple Redis publisher example.

Usage:
  python publisher.py --channel my-channel --count 5 --interval 1
  python publisher.py          # interactive: type lines to publish
"""
import argparse
import time
import redis


def main():
    p = argparse.ArgumentParser(description="Redis publisher example")
    p.add_argument("--host", "-H", default="localhost", help="Redis host")
    p.add_argument("--port", "-p", type=int, default=6379, help="Redis port")
    p.add_argument("--channel", "-c", default="my-channel", help="Channel name")
    p.add_argument("--count", "-n", type=int, default=0, help="Number of messages to publish (0 = interactive)")
    p.add_argument("--interval", "-i", type=float, default=1.0, help="Interval between messages (seconds)")
    args = p.parse_args()

    r = redis.Redis(host=args.host, port=args.port, decode_responses=True)

    if args.count > 0:
        for i in range(1, args.count + 1):
            msg = f"message {i}"
            r.publish(args.channel, msg)
            print(f"Published: {msg}")
            time.sleep(args.interval)
    else:
        print(f"default parameters: {args}")
        print(f"Interactive publisher. Publishing to channel '{args.channel}'. Type lines and press Enter.")
        try:
            while True:
                line = input()
                if not line:
                    continue
                r.publish(args.channel, line)
                print(f"Published: {line}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting publisher")


if __name__ == "__main__":
    main()
