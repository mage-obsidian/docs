import sys
from importlib import import_module

CHECKS = {
    "parity": "docs_checks.parity",
    "phrases": "docs_checks.phrases",
    "voseo": "docs_checks.voseo",
    "redirects": "docs_checks.redirects",
    "links": "docs_checks.links",
    "links_internal": "docs_checks.links_internal",
    "reference": "docs_checks.reference",
}


def main(argv):
    if len(argv) < 2 or argv[1] not in CHECKS:
        print("usage: python -m docs_checks {" + ",".join(CHECKS) + "} [args]")
        return 2
    findings = import_module(CHECKS[argv[1]]).run(argv[2:])
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
