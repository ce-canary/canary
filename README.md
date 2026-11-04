# CE Canary

Unofficial test builds of larger features and changes for CoreELEC that need wider testing before they can merge.

Each build is a CoreELEC nightly with our changes on top, and everything here is meant to go upstream to Kodi or be merged into CoreELEC. Builds strictly follow the nightlies and any feature additions or changes leave the canary once landed in CoreELEC. Each release lists the nightly it is based on and what it adds.

These builds are for testing and early feature previews. Despite extensive testing, there may be unexpected issues on devices that are outside my test coverage. Please report problems here or in the Canary builds forum post, since they may come from a change that is not in standard CoreELEC yet.

## Current testflights

**Status: active.**

- CoreELEC 22: latest build `22.0-Piers_canary_20261104`, based on the nightly of `20261103`.

- **Blu-ray menu playback:** full disc menus with more seamless clip transitions.
- **A/V sync:** vastly tighter audio and video sync with stability across playback events.
- **Screen capture:** screenshots and Hyperion ambilight for all HDR formats and output modes.

When everything here has landed in CoreELEC, this section will say there is no active canary. Use the normal nightly until the next testflight starts.

## Install

Canary builds update an existing CoreELEC install. For a fresh install, set up the box with the standard CoreELEC image first, then update to canary with the steps below.

1. Download the `.tar` from the latest [release](https://github.com/ce-canary/canary/releases) and check it against its `.sha256`.
2. Copy it to `/storage/.update` on your box and reboot.

That's the only manual step. New canary builds then show up in the CoreELEC settings under Updates > Available Versions, and CoreELEC's updater won't replace the canary with a nightly.

Canary builds run on the same devices as the matching CoreELEC nightly. Make a backup first.

## Blu-ray menus

Java (BD-J) menus need CoreELEC's normal "JRE for BD-J menus" add-on, as on any CE build.

### Top menu button

The new top menu action goes to the disc's top menu, even inside a Java (BD-J) extra where the normal menu button does nothing. If your remote has a top menu button that reaches Kodi, for example over CEC, it now does this with no setup.

To use another button, save this as `/storage/.kodi/userdata/keymaps/topmenu.xml` and restart Kodi. Replace `yourkey` with the name of your key. Any function that key already has during playback is replaced.

```xml
<keymap>
  <FullscreenVideo>
    <keyboard>
      <yourkey>PlayerControl(ShowVideoTopMenu)</yourkey>
    </keyboard>
  </FullscreenVideo>
  <VideoMenu>
    <keyboard>
      <yourkey>PlayerControl(ShowVideoTopMenu)</yourkey>
    </keyboard>
  </VideoMenu>
</keymap>
```

## A/V sync

Nothing to set up. Sync is now zeroed and doesn't shift around during playback. Your TV, AVR and speakers still add their own delay, so you may want to calibrate for your home theater with [Audio Offset Manager: Evolved](https://github.com/matthane/script.audiooffsetmanager.evolved), available in the official Kodi repo or from GitHub.

## Screen capture

Screenshots and Hyperion ambilight capture the real picture for all HDR formats and output modes, even TV-led Dolby Vision, including Profile 5 and FEL.

### Screenshots

Take a screenshot as usual, or over SSH with `kodi-send`. Shots go to your Kodi screenshot folder, `/storage/screenshots` by default. The default type is set in Settings > System > Logging > Screenshot type.

- Standard saves an SDR image up to 1080p.
- Native keeps the output resolution up to 4K, with 10-bit precision and HDR when the picture is HDR.

```
kodi-send --action="TakeScreenshot"               # the default type, with the GUI
kodi-send --action="TakeScreenshot(native)"       # Native, with the GUI
kodi-send --action="TakeScreenshot(video)"        # video only, no GUI, OSD or subtitles
kodi-send --action="TakeScreenshot(video,native)" # Native, video only
```

### Hyperion ambilight

Hyperion gets its picture from Kodi, so it needs no grabber of its own.

1. Disable the normal Hyperion add-on, then enable "Hyperion.NG (canary)" in My add-ons. It copies your existing configuration on first start.
2. In the Hyperion web UI (`http://<your box>:8090`), open Network Services and check that the Flatbuffer Server is enabled on port 19400. Those are the defaults, so a normal setup needs no change.
3. In the add-on's settings, choose what Kodi sends: Off, Video, or Video and menus (the default). You can also keep sending while a screensaver runs.

Your LED layout and other settings work as before.

## Going back to a nightly

Copy a nightly `.tar` to `/storage/.update` and reboot. Your normal add-ons and settings stay as they were.

## Reporting a problem

Follow CoreELEC's [guide to reporting an issue](https://discourse.coreelec.org/t/how-to-report-an-issue-youre-having-with-coreelec/3022) and [debug log instructions](https://wiki.coreelec.org/coreelec:debuglogs). Then open an [issue](https://github.com/ce-canary/canary/issues/new/choose) with your device, the build name, the steps and the link to your log.

## Changes by feature

| Feature | Kodi | common_drivers | CoreELEC | History |
|---|---|---|---|---|
| Blu-ray menu playback | [72 commits](https://github.com/ce-canary/xbmc/compare/base/22...topic/22/menu-playback) | [5 commits](https://github.com/ce-canary/common_drivers/compare/topic/22/av-sync...topic/22/menu-playback) | [17 commits](https://github.com/ce-canary/CoreELEC/compare/topic/22/screen-capture...topic/22/menu-playback) | [history](https://github.com/ce-canary/canary/commits/main/series/22/menu-playback) |
| A/V sync | [45 commits](https://github.com/ce-canary/xbmc/compare/topic/22/menu-playback...topic/22/av-sync) | [4 commits](https://github.com/ce-canary/common_drivers/compare/base/22...topic/22/av-sync) | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/av-sync) |
| Screen capture | [23 commits](https://github.com/ce-canary/xbmc/compare/topic/22/av-sync...topic/22/screen-capture) | [12 commits](https://github.com/ce-canary/common_drivers/compare/topic/22/menu-playback...topic/22/screen-capture) | [5 commits](https://github.com/ce-canary/CoreELEC/compare/base/22...topic/22/screen-capture) | [history](https://github.com/ce-canary/canary/commits/main/series/22/screen-capture) |
| Canary-only changes | none | none | [3 commits](https://github.com/ce-canary/CoreELEC/compare/topic/22/menu-playback...topic/22/canary-only) | [history](https://github.com/ce-canary/canary/commits/main/series/22/canary-only) |

Each link shows that feature's commits and combined diff for the current build. History shows how a feature changed between builds.

**Canary-only changes:** what the canary image itself needs. These never go upstream.

## Credits

The Blu-ray menu and A/V sync work draws on [SamuriHL](https://github.com/SamuriHL)'s public builds and branches. His commits showed several of the defects, mechanisms and design ideas used here, and he reached a number of these problems first. Pull requests credit him per change.

## Source

Every build has a tag in the repositories it changes, listed in its release notes. `series/` holds our changes as patch files, one folder per feature, so its history shows what changed between builds.

- [CoreELEC](https://github.com/ce-canary/CoreELEC): the build system and packaging
- [Kodi](https://github.com/ce-canary/xbmc): CoreELEC's Kodi
- [common_drivers](https://github.com/ce-canary/common_drivers): Amlogic kernel drivers
- [linux-amlogic](https://github.com/ce-canary/linux-amlogic): the kernel
- [media_modules](https://github.com/ce-canary/media_modules-aml): video decoder drivers
