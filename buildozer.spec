[app]

title = Kodi Calc
package.name = timbercalc
package.domain = org.femunu12

source.dir = .
source.include_exts = py,png,jpg,kv

version = 0.1

# Added pillow (essential for KivyMD icons/images)
requirements = python3,kivy==2.3.0,kivymd,pillow

icon.filename = icon.png

# LOCKS THE VIEW TO VERTICAL
orientation = portrait

fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1

[app:android]

# FIXES THE SECURITY THREAT WARNING (Targets Android 13)
android.api = 33
android.minapi = 21

# Includes both modern 64-bit and older 32-bit support
android.archs = arm64-v8a, armeabi-v7a

# MANDATORY for GitHub Actions
android.accept_sdk_license = True
