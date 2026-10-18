#!/usr/bin/env python3
"""Rebrand a checkout of ZalithLauncher2 as "Lunaro Client".
Usage: python3 apply_lunaro.py <path-to-ZalithLauncher2-checkout>
Every edit asserts that the text it expects is really there, so a changed
upstream makes the build fail loudly instead of silently producing a half-patched app.
"""
import re, shutil, sys, pathlib

root = pathlib.Path(sys.argv[1]).resolve()
here = pathlib.Path(__file__).resolve().parent
app = root / "ZalithLauncher"
main = app / "src/main"
kt = main / "java/com/movtery/zalithlauncher"

def edit(path, fn):
    t = path.read_text(encoding="utf-8"); n = fn(t)
    assert n != t, f"no change made in {path}"
    path.write_text(n, encoding="utf-8")

def sub1(t, old, new):
    assert old in t, f"expected text not found: {old[:60]!r}"
    return t.replace(old, new, 1)

# 1. Name
edit(app / "gradle.properties", lambda t: sub1(sub1(t, "launcher_app_name=Zalith Launcher", "launcher_app_name=Lunaro Client"),
                                              "launcher_short_name=ZL2", "launcher_short_name=Lunaro"))
# 2. Own package id so it installs next to Zalith (code namespace stays untouched)
edit(app / "build.gradle.kts", lambda t: sub1(t, 'applicationIdSuffix = ".v2"', 'applicationIdSuffix = ".lunaro"'))
# 3. Default: Lunaro theme, always (not wallpaper colours), dark mode on
edit(kt / "setting/AllSettings.kt", lambda t: sub1(t,
    "if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) ColorThemeType.DYNAMIC\n        else ColorThemeType.EMBERMIRE",
    "ColorThemeType.EMBERMIRE"))
edit(kt / "setting/AllSettings.kt", lambda t: sub1(t,
    'enumSetting("launcherDarkMode", DarkMode.FollowSystem)', 'enumSetting("launcherDarkMode", DarkMode.Enable)'))

# 4. Lunaro palette replaces the first ("embermire") column of every colour row
dark = dict(primary="C9B6FF", onPrimary="2E1A66", primaryContainer="5B3FD0", onPrimaryContainer="FFFFFF",
    secondary="C2C6F2", onSecondary="2A2F5B", secondaryContainer="3B4170", onSecondaryContainer="DDE0FF",
    tertiary="7FD7F2", onTertiary="00363F", tertiaryContainer="1B6B7D", onTertiaryContainer="C0F1FF",
    background="0D0B1A", onBackground="E6E1F5", surface="0D0B1A", onSurface="E6E1F5",
    surfaceVariant="2D2A45", onSurfaceVariant="C9C4DE", outline="938FA8", outlineVariant="474360",
    inverseSurface="E6E1F5", inverseOnSurface="312E42", inversePrimary="5B3FD0",
    surfaceDim="0D0B1A", surfaceBright="36334D", surfaceContainerLowest="08060F", surfaceContainerLow="15122A",
    surfaceContainer="191630", surfaceContainerHigh="241F3C", surfaceContainerHighest="2F2A48")
light = dict(primary="5B3FD0", onPrimary="FFFFFF", primaryContainer="E6DEFF", onPrimaryContainer="1A0A5C",
    secondary="5B5D8A", onSecondary="FFFFFF", secondaryContainer="E1E0FF", onSecondaryContainer="171A44",
    tertiary="006A7D", onTertiary="FFFFFF", tertiaryContainer="B6EBFF", onTertiaryContainer="001F27",
    background="FCF8FF", onBackground="1C1B22", surface="FCF8FF", onSurface="1C1B22",
    surfaceVariant="E5E0F0", onSurfaceVariant="47445A", outline="787590", outlineVariant="C9C4DE",
    inverseSurface="312E42", inverseOnSurface="F3EFFF", inversePrimary="C9B6FF",
    surfaceDim="DCD8E6", surfaceBright="FCF8FF", surfaceContainerLowest="FFFFFF", surfaceContainerLow="F6F2FF",
    surfaceContainer="F0ECFA", surfaceContainerHigh="EAE6F4", surfaceContainerHighest="E5E1EF")
def colors(t):
    done = 0
    for suffix, pal in (("Dark", dark), ("Light", light)):
        for name, hexv in pal.items():
            pat = re.compile(rf"(^val {name}{suffix} = ColorTheme\()Color\(0x[0-9A-Fa-f]{{8}}\)", re.M)
            t, k = pat.subn(rf"\1Color(0xFF{hexv})", t); assert k == 1, f"{name}{suffix}"; done += 1
    assert done == len(dark) + len(light)
    return t
edit(kt / "ui/theme/Color.kt", colors)
edit(kt / "ui/theme/NativeThemeUtils.kt", lambda t: sub1(t,
    "ColorThemeType.EMBERMIRE -> if (darkTheme) 0xFFFFB598.toInt() else 0xFFA63A17.toInt()",
    "ColorThemeType.EMBERMIRE -> if (darkTheme) 0xFFC9B6FF.toInt() else 0xFF5B3FD0.toInt()"))

# 5. Icons
res = main / "res"
for f in (here / "res").rglob("*"):
    if f.is_file():
        dst = res / f.relative_to(here / "res"); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy(f, dst)
print("Lunaro Client patch applied to", root)
