# Odin demo · Project Cerberus

**Open the demo: [purpleninjaradish.github.io/Odin-2](https://purpleninjaradish.github.io/Odin-2/)**

Odin, the Secure Student Analyzer, version 0.6.0-alpha. Every student and teacher in this demo is invented. Never enter real student information here: the real Odin runs offline on the Project Cerberus server at school.

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

## Things to try

- **Student:** a student's levels, primary and secondary needs, and support tier.
- **Focus:** the weekly focus groups, with pre- and post-checks.
- **Practice:** open a sheet, then **Start on this device** for the locked student mode.
- **Fluency:** **Watch a sample reading** shows the reading screen with the voice guide. Speaking into the microphone works only in a browser that can recognize speech on the device itself, such as an up-to-date Google Chrome; iPhones and iPads can't yet, so there the teacher scores the reading.

## What's in this repository

| File | What it is |
| --- | --- |
| `index.html` | The demo page, with the invented students built in |
| `manifest.webmanifest`, `icons/`, `sw.js`, `offline.html` | What lets the demo install as an app. The service worker stores only the offline page and an icon |
| `qr-code.png` | The QR code above |
| `.github/workflows/static.yml` | Publishes the repository to GitHub Pages on every push to `main` |
| `server.py`, `Dockerfile`, `.dockerignore` | From an earlier hosted demo (version 0.2). The page above doesn't use them |

The full Odin server, with its wiki and tests, lives in a separate private repository.
