from helpers.utils.printer import colorFormatter, inp, log
from time import sleep
import traceback
from scripts.OLT import olt


def main():
    try:
        while True:
                olt()

    except KeyboardInterrupt:
        resp = colorFormatter("Saliendo...", "warning")
        log(resp)
        sleep(0.5)
    except Exception:
        resp = colorFormatter(f"Error At : {traceback.format_exc()}", "fail")
        log(resp)
        sleep(10)


if __name__ == "__main__":
    main()
