"""Simple Redis subscriber example.

Usage:
  python subscriber.py --channel my-channel
"""
import argparse
import redis


def main():
    p = argparse.ArgumentParser(description="Redis subscriber example")
    p.add_argument("--host", "-H", default="localhost", help="Redis host")
    p.add_argument("--port", "-p", type=int, default=6379, help="Redis port")
    p.add_argument("--channel", "-c", default="my-channel", help="Channel name")
    args = p.parse_args()

    r = redis.Redis(host=args.host, port=args.port, decode_responses=True)

    pubsub = r.pubsub(ignore_subscribe_messages=False)
    pubsub.subscribe(args.channel)
    print(f"Subscribed to channel '{args.channel}'. Waiting for messages...")

    try:
        for message in pubsub.listen():
            print(f"Received raw message: {message}")
            # When decode_responses=True, data is already a str
            if message is None:
                print("hitted None message, skipping")
                continue
            data = message.get("data")
            if data is None:
                continue
            print(f"Received: {data}")
    except KeyboardInterrupt:
        print("\nExiting subscriber")
    finally:
        pubsub.close()


if __name__ == "__main__":
    main()
