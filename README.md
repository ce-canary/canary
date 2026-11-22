# CE Canary

Unofficial test builds of larger features and changes for CoreELEC that need wider testing before they can merge.

Each build is a CoreELEC nightly with our changes on top, and everything here is meant to go upstream to Kodi or be merged into CoreELEC. Builds strictly follow the nightlies and any feature additions or changes leave the canary once landed in CoreELEC. Each release lists the nightly it is based on and what it adds.

These builds are for testing and early feature previews. Despite extensive testing, there may be unexpected issues on devices that are outside my test coverage. Please report problems here or in the [Canary builds forum post](https://discourse.coreelec.org/t/ce-canary-unofficial-test-builds-of-upcoming-features/60378), since they may come from a change that is not in standard CoreELEC yet.

## Current testflights

**Status: active.**

- CoreELEC 22: latest build `22.0-Piers_canary_20261119`, based on the nightly of `20261119`.

- **Small fixes:** independent fixes that don't belong to any feature.
- **Blu-ray menu playback:** full disc menus with more seamless clip transitions.
- **A/V sync:** vastly tighter audio and video sync with stability across playback events.
- **Screen capture:** screenshots and Hyperion ambilight for all HDR formats and output modes.
- **Dolby Vision FEL playback:** FEL titles play through to the end, and Blu-ray menus no longer turn black on FEL clips.
- **Dolby Vision output:** Dolby Vision no longer turns purple when playback starts from a refresh rate the TV can't show in Dolby Vision.
- **Faster mode switches:** playback starts sooner, the TV blanks for less time at a mode change, and Blu-ray menus keep one output mode for the whole disc.
- **Seamless video playlists:** the next video in a playlist starts without a black screen, and streamed items join in a moment.
- **Atmos passthrough continuity:** No more Atmos pop-up on pause, seek and chapter skips.
- **DVD menus:** every DVD menu page shows, highlights follow the remote, and titles play out and resume where you left.

When everything here has landed in CoreELEC, this section will say there is no active canary. Use the normal nightly until the next testflight starts.

## Install

Canary builds update an existing CoreELEC install. For a fresh install, set up the box with the standard CoreELEC image first, then update to canary with the steps below.

1. Download the `.tar` from the latest [release](https://github.com/ce-canary/canary/releases) and check it against its `.sha256`.
2. Copy it to `/storage/.update` on your box and reboot.

That's the only manual step. New canary builds then show up in the CoreELEC settings under Updates > Available Versions, and CoreELEC's updater won't replace the canary with a nightly.

Canary builds run on the same devices as the matching CoreELEC nightly. Make a backup first.

## Small fixes

- Audio offset add-ons see an audio track change made by a Blu-ray disc's own menu right away.
- Progressive VC-1 video decodes straight into its display buffers, which removes a cause of short horizontal lines on moving pictures. Thanks to alexscotti, whose Symphony build found the cause.
- VC-1 video plays smoothly instead of stuttering.

Nothing to set up.

## Blu-ray menu playback

Play a disc with its full menus, HDMV and Java (BD-J) alike, with more seamless clip transitions. Java menus need CoreELEC's normal "JRE for BD-J menus" add-on, as on any CE build.

On Blu-ray discs with Java menus, the disc's own timer now follows the picture on screen. It stops during a pause, stays in step after a seek and ends with the episode.

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

Sync is now zeroed and doesn't shift around during playback. Nothing to set up. Your TV, AVR and speakers still add their own delay, so you may want to calibrate for your home theater with [Audio Offset Manager: Evolved](https://github.com/matthane/script.audiooffsetmanager.evolved), available in the official Kodi repo or from GitHub. The audio offset now moves in 5 ms steps instead of 25 ms, so calibration lands closer.

## Screen capture

Screenshots and Hyperion ambilight capture the real picture for all HDR formats and output modes, even TV-led Dolby Vision, including Profile 5 and FEL.

Screenshots, Hyperion and other capture add-ons run at the same time without taking frames from each other. Hyperion keeps its picture through refresh rate and HDR switches instead of dropping to its idle effect.

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
3. In the add-on's settings, choose what Kodi sends: Off, Playback only, or Playback and menus (the default). You can also keep sending while a screensaver runs.

Your LED layout and other settings work as before.

## Dolby Vision FEL playback

Dolby Vision FEL titles play through to the end, and Blu-ray menus no longer turn black when a menu plays an FEL clip. Nothing to set up.
FEL titles no longer drop to HDR10 for a moment at start and seek.

## Dolby Vision output

Dolby Vision no longer turns purple when playback starts from a refresh rate the TV can't show in Dolby Vision, for example right after a 120 Hz SDR clip or menu. The output now picks the right Dolby Vision colour format for the mode it switches to. Nothing to set up.

## Faster mode switches

Playback starts sooner and the TV blanks for less time when the output mode changes. Short Blu-ray menu clips, Dolby Vision clip changes and menu selections are all faster, and soft-telecine DVDs now set the mode once and stay at 59.94 Hz.

Blu-ray menus now keep the main feature's resolution and HDR or Dolby Vision format for every intro, menu and extra, so the TV no longer switches back and forth while you navigate. It is on by default as "Keep the disc's output format", next to the other HDR conversion settings. Turn it off to let each clip use its own format. The refresh rate still follows each video.

## Seamless video playlists

The next video in a playlist now plays on in the running player. The last picture stays up until the next one starts, and the TV keeps its mode and HDR format when the items match. Items at another frame rate still switch the refresh rate.

The next item opens while the current one finishes, for local and network files and for streaming add-ons that use InputStream Adaptive, so joins between streamed items are much shorter. Videos also play out to their last frame.

Adaptive streams no longer freeze a few seconds into an item. They start at a quality the connection can carry, and the TV mode is set for the stream's best quality from the start. Nothing to set up.

## Atmos passthrough continuity

Dolby Digital Plus Atmos and Dolby TrueHD Atmos passthrough now keep the audio signal running through pause, seek and chapter skips. TVs that show the Dolby Atmos notice whenever the signal restarts no longer do. For long pauses, set Keep audio device alive to Always to avoid any other unwanted notices.

## DVD menus

DVD menus now behave like a disc player. Every menu page shows its picture, button highlights follow the remote on looping menus, and a title plays to its end before the disc goes back to its menu. Stop is instant, and Resume from the menu or after a stop picks up at the picture you left. Nothing to set up.

## Going back to a nightly

Copy a nightly `.tar` to `/storage/.update` and reboot. Your normal add-ons and settings stay as they were.

## Reporting a problem

First, [go back to a standard nightly](#going-back-to-a-nightly) and see if the problem is still there. If it is, it isn't from the canary, so report it to CoreELEC as usual. If it only happens on the canary, report it here. Features that only work on the canary can skip this step.

Follow CoreELEC's [guide to reporting an issue](https://discourse.coreelec.org/t/how-to-report-an-issue-youre-having-with-coreelec/3022) and [debug log instructions](https://wiki.coreelec.org/coreelec:debuglogs). Then post in the [forum thread](https://discourse.coreelec.org/t/ce-canary-unofficial-test-builds-of-upcoming-features/60378) or open an [issue](https://github.com/ce-canary/canary/issues/new/choose) with your device, the build name, the steps and the link to your log.

## Changes by feature

| Feature | Kodi | common_drivers | media_modules-aml | CoreELEC | History |
|---|---|---|---|---|---|
| Small fixes | [2 commits](https://github.com/ce-canary/xbmc/compare/base/22...topic/22/fixes) | [1 commit](https://github.com/ce-canary/common_drivers/compare/base/22...topic/22/fixes) | [2 commits](https://github.com/ce-canary/media_modules-aml/compare/base/22...topic/22/fixes) | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/fixes) |
| Blu-ray menu playback | [70 commits](https://github.com/ce-canary/xbmc/compare/topic/22/fixes...topic/22/menu-playback) + [2 commits](https://github.com/ce-canary/xbmc/compare/topic/22/seamless-playlist...topic/22/bdj-media-time) | [6 commits](https://github.com/ce-canary/common_drivers/compare/topic/22/av-sync...topic/22/menu-playback) | none | [20 commits](https://github.com/ce-canary/CoreELEC/compare/topic/22/screen-capture...topic/22/menu-playback) | [history](https://github.com/ce-canary/canary/commits/main/series/22/menu-playback) |
| A/V sync | [43 commits](https://github.com/ce-canary/xbmc/compare/topic/22/menu-playback...topic/22/av-sync) | [2 commits](https://github.com/ce-canary/common_drivers/compare/topic/22/dv-output...topic/22/av-sync) | none | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/av-sync) |
| Screen capture | [32 commits](https://github.com/ce-canary/xbmc/compare/topic/22/av-sync...topic/22/screen-capture) | [39 commits](https://github.com/ce-canary/common_drivers/compare/topic/22/menu-playback...topic/22/screen-capture) | none | [5 commits](https://github.com/ce-canary/CoreELEC/compare/base/22...topic/22/screen-capture) | [history](https://github.com/ce-canary/canary/commits/main/series/22/screen-capture) |
| Dolby Vision FEL playback | [6 commits](https://github.com/ce-canary/xbmc/compare/topic/22/screen-capture...topic/22/fel-playback) | none | [8 commits](https://github.com/ce-canary/media_modules-aml/compare/topic/22/fixes...topic/22/fel-playback) | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/fel-playback) |
| Dolby Vision output | none | [2 commits](https://github.com/ce-canary/common_drivers/compare/topic/22/fixes...topic/22/dv-output) | none | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/dv-output) |
| Faster mode switches | [23 commits](https://github.com/ce-canary/xbmc/compare/topic/22/fel-playback...topic/22/mode-switch-time) | [1 commit](https://github.com/ce-canary/common_drivers/compare/topic/22/screen-capture...topic/22/mode-switch-time) | [1 commit](https://github.com/ce-canary/media_modules-aml/compare/topic/22/fel-playback...topic/22/mode-switch-time) | [1 commit](https://github.com/ce-canary/CoreELEC/compare/topic/22/canary-only...topic/22/mode-switch-time) | [history](https://github.com/ce-canary/canary/commits/main/series/22/mode-switch-time) |
| Seamless video playlists | [40 commits](https://github.com/ce-canary/xbmc/compare/topic/22/mode-switch-time...topic/22/seamless-playlist) | none | [2 commits](https://github.com/ce-canary/media_modules-aml/compare/topic/22/mode-switch-time...topic/22/seamless-playlist) | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/seamless-playlist) |
| Atmos passthrough continuity | [12 commits](https://github.com/ce-canary/xbmc/compare/topic/22/bdj-media-time...topic/22/passthrough-continuity) | none | none | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/passthrough-continuity) |
| DVD menus | [17 commits](https://github.com/ce-canary/xbmc/compare/topic/22/passthrough-continuity...topic/22/dvd-menus) | none | none | none | [history](https://github.com/ce-canary/canary/commits/main/series/22/dvd-menus) |
| Canary-only changes | none | none | none | [4 commits](https://github.com/ce-canary/CoreELEC/compare/topic/22/menu-playback...topic/22/canary-only) | [history](https://github.com/ce-canary/canary/commits/main/series/22/canary-only) |

Each link shows that feature's commits and combined diff for the current build. History shows how a feature changed between builds.

**Canary-only changes:** what the canary image itself needs. These never go upstream.

## Credits

The Blu-ray menu, A/V sync and Dolby Vision FEL work draws on [SamuriHL](https://github.com/SamuriHL)'s public builds and branches. Their commits showed several of the defects, mechanisms and design ideas used here, and they reached a number of these problems first. Pull requests credit them per change.

## Source

Every build has a tag in the repositories it changes, listed in its release notes. `series/` holds our changes as patch files, one folder per feature, so its history shows what changed between builds.

- [CoreELEC](https://github.com/ce-canary/CoreELEC): the build system and packaging
- [Kodi](https://github.com/ce-canary/xbmc): CoreELEC's Kodi
- [common_drivers](https://github.com/ce-canary/common_drivers): Amlogic kernel drivers
- [linux-amlogic](https://github.com/ce-canary/linux-amlogic): the kernel
- [media_modules](https://github.com/ce-canary/media_modules-aml): video decoder drivers
