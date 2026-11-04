#!/usr/bin/env python3
"""Add a canary build to the channel file that CoreELEC's updater reads.

The file has the same shape as https://update.coreelec.org/releases.php. The updater downloads
`url` + `file.name`, and shows the part of `file.name` that `prettyname_regex` captures, here the
tag of the release that holds the tar:

  url        https://github.com/ce-canary/canary/releases/download/
  file.name  <tag>/CoreELEC-Amlogic-no.aarch64-22.0-Piers_canary_<date>.tar

The channel name must be <word>-<number>: the updater sorts channels of one <word> by
that number, and a name like CE-Canary-22 breaks the list once a second CE-* channel exists.
`releases` keys must be integers as strings; the highest is listed first. Each CoreELEC major
has its own file and channel, taken from the tar name unless given.

The assembly tool calls add_build for each build. By hand:

  make-channel.py --tag <tag> --tar <path> [--out canary-<major>.json] [--channel Canary-<major>]
                  [--url <base>] [--keep N]
"""
import argparse
import json
import os
import re

URL = "https://github.com/ce-canary/canary/releases/download/"
REGEX = r"(^.*)\/.*"
TAR = re.compile(r"CoreELEC-(.+\.(?:aarch64|arm))-(\d+)\..*\.tar$")
CHANNEL = re.compile(r"[^-]+-[0-9.]+$")


def row_tag(row):
    return row["file"]["name"].split("/")[0]


def check_channel(path, tag, tar_name):
    """Read a channel file back the way get_available_builds does. Stops on the first fault."""
    with open(path) as f:
        doc = json.load(f)
    want = "%s/%s" % (tag, tar_name)
    found = False
    for channel, chan in doc.items():
        if not CHANNEL.match(channel):
            raise SystemExit("channel must be <word>-<number>: %s" % channel)
        if not chan["url"].endswith("/"):
            raise SystemExit("%s: url must end in /: %s" % (channel, chan["url"]))
        regex = re.compile(chan["prettyname_regex"])
        for arch, proj in chan["project"].items():
            for key, row in proj["releases"].items():
                name = row["file"]["name"]
                pretty = regex.findall(name)
                tar = TAR.match(name.split("/")[-1])
                if not key.isdigit() or not pretty or name.count("/") != 1 or \
                        pretty[0] != row_tag(row) or not tar or tar.group(1) != arch:
                    raise SystemExit("%s: bad release %s: %s" % (channel, key, name))
                found = found or name == want
    if not found:
        raise SystemExit("%s does not list %s" % (path, want))


def add_build(out, tag, tar_name, size, channel, url=URL, keep=5, gone=lambda tag: False):
    """Add or refresh one build. A tag `gone` says never reached a release loses its row."""
    m = TAR.match(tar_name)
    if not m:
        raise SystemExit("not a CoreELEC tar name: %s" % tar_name)
    if "/" in tag:
        raise SystemExit("tag has a slash: %s" % tag)
    arch = m.group(1)

    doc = {}
    if os.path.exists(out):
        with open(out) as f:
            doc = json.load(f)
    chan = doc.setdefault(channel, {"url": url, "prettyname_regex": REGEX, "project": {}})
    chan["url"] = url
    proj = chan["project"].setdefault(arch, {"displayName": arch, "releases": {}})
    rows = [r for _, r in sorted(proj["releases"].items(), key=lambda kv: int(kv[0]))
            if row_tag(r) == tag or not gone(row_tag(r))]
    new = {"file": {"name": "%s/%s" % (tag, tar_name), "size": size}}
    same = [i for i, r in enumerate(rows) if row_tag(r) == tag]
    if same:
        rows[same[0]] = new
    else:
        rows.append(new)
    rows = rows[-keep:]
    proj["releases"] = {str(i): r for i, r in enumerate(rows)}

    tmp = out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    try:
        check_channel(tmp, tag, tar_name)
    except SystemExit:
        os.remove(tmp)
        raise
    os.replace(tmp, out)
    print("%s: %s %s, %d build(s)" % (out, channel, arch, len(rows)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--tar", required=True)
    ap.add_argument("--out")
    ap.add_argument("--channel")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--keep", type=int, default=5, help="builds listed, newest first")
    a = ap.parse_args()

    base = os.path.basename(a.tar)
    m = TAR.match(base)
    if not m:
        raise SystemExit("not a CoreELEC tar name: %s" % base)
    add_build(a.out or "canary-%s.json" % m.group(2), a.tag, base, os.path.getsize(a.tar),
              a.channel or "Canary-%s" % m.group(2), a.url, a.keep)


if __name__ == "__main__":
    main()
