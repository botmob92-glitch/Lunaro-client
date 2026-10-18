# Lunaro Client — Minecraft Java Edition for Android

A rebranded build of [ZalithLauncher2](https://github.com/ZalithLauncher/ZalithLauncher2)
(GPL-3.0) with its own name, moon icon and dark purple theme.
Lunaro Client is an independent project. It is not affiliated with Lunar Client, Mojang or Microsoft.

## Get the APK (works from a phone browser)
1. Create a free GitHub account and a new empty repository (e.g. `lunaro-client`).
2. Add the 4 text files of this project with the same paths (on GitHub: Add file → Create new file; typing `/` in the name makes folders):
   `.github/workflows/build-lunaro-apk.yml`, `patch/apply_lunaro.py`, `patch/make_icons.py`, `README.md`.
   (On a PC you can simply drag the whole folder in.)
3. Open the **Actions** tab → **Build Lunaro Client APK** → **Run workflow** (leave `arm64`).
4. After ~10-25 minutes open the finished run and download the **Lunaro-Client-apk-arm64** artifact (a zip containing the APK).
5. Unzip, install the APK (allow "install unknown apps"). It installs next to Zalith Launcher (different package id).

## What the patch changes
- App name -> Lunaro Client, new package id suffix `.lunaro`
- New moon icon (original artwork)
- Default theme: dark + Lunaro purple palette (no wallpaper colours); you can still change themes in Settings
- Nothing else: all launcher/game code is upstream ZalithLauncher2 at a pinned commit (see workflow)

## License
GPL-3.0, same as upstream. If you share the built APK, also share this repository (it is the source of the changes) and keep the upstream credits.
