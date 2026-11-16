# Odin demo · Project Cerberus

**Open the demo: [purpleninjaradish.github.io/Odin-2](https://purpleninjaradish.github.io/Odin-2/)**

Odin, the Secure Student Analyzer, version 0.7.0-alpha. Every student and teacher in this demo is invented. Never enter real student information here: the real Odin runs offline on the Project Cerberus server at school.

## Test it on another device

Scan this code with the phone's or tablet's camera, or type the address above:

![QR code for https://purpleninjaradish.github.io/Odin-2/](qr-code.png)

To install it as an app with its own icon:

| Device | How |
| --- | --- |
| iPhone or iPad | Open the link in **Safari**, tap **Share**, then **Add to Home Screen** |
| Android | Open the link in **Chrome**, tap **⋮**, then **Install app** (or **Add to Home screen**) |
| Computer | In Chrome or Edge, click the install button at the right of the address bar |

On a phone, the bar at the bottom holds Class, Student, Focus, Practice and Fluency, and **More** has the other views. **Menu** (top right) has the class, Reading or Math, and Codes or Names.

**Each device keeps its own changes.** Marks, checks and readings you make in the demo stay in that browser on that device. Nothing is shared between devices, and nothing is sent anywhere. To start over on a device, clear this site's data in the browser's settings.

## Odin app for Android (test)

On Android, the **Odin app** adds the microphone to fluency practice. When a student stops on a word or misreads it, the voice says the word and asks the student to say it. Odin listens, waits for the answer, and goes on. It uses Android's own **on-device** speech recognition, so the voice never leaves the phone, and nothing is recorded.

**Download: [odin-android.apk](https://purpleninjaradish.github.io/Odin-2/odin-android.apk)**, or scan this on the Android phone or tablet:

![QR code for the Odin app for Android](qr-android.png)

1. Open the download. Android asks to allow installing apps from this source (the browser or Files): allow it, then **Install**. If Google Play Protect warns about an unknown app, choose **More details**, then **Install anyway**: it is a test build, signed with a test key, not from the Play Store.
2. Open **Odin** and choose **Try the demo (invented students)**.
3. Open **Fluency**. The status line says whether this device can recognize speech on the device. If it offers **Set up speech on this device**, press it once (a one-time download from Google).
4. Press **Test the microphone**, allow the microphone, and say a sentence.
5. On a student's row, press **Open**, then **Practice on this device** and **Start practice**. Read the passage aloud. Stop on a word, or misread one, to hear the voice help and wait for you to say it.

The microphone needs **Android 12 or newer** with Google's speech services. On older devices the app still opens Odin, and fluency uses **Teacher scores**. For real students, the app opens the school's Project Cerberus server instead (type its `https://` address), only with the school's written approval.

## Things to try

- **Student:** a student's levels, primary and secondary needs, and support tier.
- **Focus:** the weekly focus groups, with pre- and post-checks.
- **Practice:** open a sheet, then **Start on this device** for the locked student mode.
- **Fluency:** **Watch a sample reading** shows the reading screen with the voice guide. Speaking into the microphone works where speech is recognized on the device itself: an up-to-date Google Chrome on a computer, or the [Odin app for Android](#odin-app-for-android-test). iPhones and iPads can't yet, so there the teacher scores the reading.

## What's in this repository

| File | What it is |
| --- | --- |
| `index.html` | The demo page, with the invented students built in |
| `manifest.webmanifest`, `icons/`, `sw.js`, `offline.html` | What lets the demo install as an app. The service worker stores only the offline page and an icon |
| `qr-code.png` | The QR code above |
| `odin-android.apk`, `qr-android.png` | The Odin app for Android (test build) and its QR code |
| `.github/workflows/static.yml` | Publishes the repository to GitHub Pages on every push to `main` |
| `server.py`, `Dockerfile`, `.dockerignore` | From an earlier hosted demo (version 0.2). The page above doesn't use them |

The full Odin server, with its wiki and tests, lives in a separate private repository.
