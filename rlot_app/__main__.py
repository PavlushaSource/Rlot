import sys

import rlot_app

if __name__ == "__main__":
    try:
        rlot_app.main()
    except KeyboardInterrupt:
        print("\nControl-C pressed")
        sys.exit(1)
