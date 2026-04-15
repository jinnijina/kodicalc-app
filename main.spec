[app]
title = My KivyMD App
package.name = kodicalc
package.domain = org.femunu12
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# CRITICAL: Requirements for KivyMD
requirements = python3, kivy==2.3.0, kivymd, pillow, requests

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
