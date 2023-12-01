import rlot
import sys

if __name__ == "__main__":
    try:
        rlot.main()
    except KeyboardInterrupt:
        print("\nControl-C pressed")
        sys.exit(1)