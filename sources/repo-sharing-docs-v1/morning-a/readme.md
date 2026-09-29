# Morning reader

An Android app that replaces a morning scroll through Twitter and blogs with a
finite reading session. It serves public-domain books as self-contained 5–15
minute blocks, mixed with long blog posts from your feeds and short videos about
the books. A block can start only if it fits in the time left in today's budget
(45 minutes by default), so the session ends instead of refilling.

This is a personal project shared as source code. There are no prebuilt APKs: you
build the app yourself with your own API key.

## How it works

- **Blocks.** A block is a book passage of about 5–15 minutes, a blog post of 5
  minutes or more, or a video of 10 minutes or less. Short stories and poems are
  never split, so a block is one or more whole stories or a few whole poems.
- **Today's session.** The home screen offers blocks from several books and blogs,
  each with a one-line hook and a time estimate based on your measured reading
  speed. The block in progress can always be finished, even past the budget.
- **Explain.** Select text and tap Explain to get a definition of one or two words,
  or an explanation of a longer passage, in the language of the book.
- **Music.** Each block has a Spotify AI Playlist prompt. The app copies it and
  opens Spotify, where you paste it.

The work is split between two places:

- **Your computer** builds a *book pack* for each book once (`./pack`): it
  downloads the book from [Project Gutenberg](https://www.gutenberg.org/), using
  the [Standard Ebooks](https://standardebooks.org/) edition when one exists, asks
  Gemini to cut it into blocks with hooks and recaps, optionally picks YouTube
  videos, and copies the pack to the phone over `adb`.
- **The phone** stores the packs, checks your blog feeds every 12 hours, and calls
  Gemini only for Explain and for blog-post hooks. Mornings don't need the computer.

The pack format is documented in [`docs/book-pack.md`](docs/book-pack.md).

## What you need

- An Android phone running Android 12 or later, with
  [USB or wireless debugging](https://developer.android.com/tools/adb#Enabling)
  turned on.
- A computer with [JDK 17](https://adoptium.net/temurin/releases/?version=17), the
  Android SDK (installed with [Android Studio](https://developer.android.com/studio)
  or the command-line tools), `adb`, and [uv](https://docs.astral.sh/uv/). It has
  been used only on macOS, but nothing in it is Mac-specific.
- An [OpenRouter](https://openrouter.ai/) API key. The app uses
  `google/gemini-3.8-flash`.
- Optionally, a YouTube Data API key, for videos.

## Setup

1. Copy `.env.example` to `.env` and fill in your keys.
   - **OpenRouter:** create a key at
     [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys). Give it a
     credit limit, because the key is compiled into the app (see
     [Keep your key private](#keep-your-key-private)).
   - **YouTube (optional):** in the
     [Google Cloud console](https://console.cloud.google.com/), create a project,
     enable the
     [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com),
     and create an API key under APIs & Services → Credentials. Without it, books
     are built without videos.
2. Point Gradle at the SDK, either with `ANDROID_HOME` or a `local.properties` file
   containing `sdk.dir=/path/to/Android/sdk`.
3. Build and install with the phone connected:

   ```bash
   ./gradlew assembleDebug
   adb install -r app/build/outputs/apk/debug/app-debug.apk
   ```

4. Open the app once, then add books and feeds as below.

## Add books

```bash
./pack search "tale of two cities"   # list Gutenberg matches with their ids
./pack add 98                        # build and push by Gutenberg id
./pack add "tale of two cities"      # or build the top search match
./pack videos                        # add videos to packs built without them
./pack push                          # re-push every built pack
```

The app loads new packs when it opens or when you tap refresh. `./pack` uses
`adb` from your `PATH`; set `ADB` in `.env` to use a different command.

`./pack starter` builds the author's first shelf of eight books (Middlemarch,
Frankenstein, Anna Karenina, and others). Edit `STARTER` in
[`packer/__main__.py`](packer/__main__.py) to make it yours.

**Cost and time.** A pack costs about $0.02–0.65 in Gemini calls, roughly $0.13
per 100,000 words, and takes about a minute. Finding videos uses 500 of YouTube's
10,000 free daily quota units, so about 20 books a day can get videos; books
built after the quota runs out get them later with `./pack videos`.

## Add blog feeds

In the app, Settings adds and removes single feeds and imports an OPML file (for
example a [Feedly export](https://docs.feedly.com/article/52-how-can-i-export-my-sources-and-feeds-through-opml)).
You can also push an OPML file from the computer with `./pack opml feeds.opml`.
Only posts of 5 minutes or more are kept.

## Keep your key private

The OpenRouter key is compiled into the APK, and anyone with the APK file can
extract it. Install the app only on your own phone, don't share the built APK, and
keep a credit limit on the key.

## Project files

- `app/` — the Android app (Kotlin, Jetpack Compose).
- `packer/` and `./pack` — book pack builder (Python).
- `docs/book-pack.md` — the book pack format.
- `DECISIONS.md` — design decisions and their reasons.
- `cache/` and `packs/` are ignored: downloads, built packs, and personal lists.

## License

The code is under the [MIT License](LICENSE). The bundled Literata font is under
the SIL Open Font License ([`licenses/literata-OFL.txt`](licenses/literata-OFL.txt)).
Books come from Project Gutenberg and Standard Ebooks; check their terms before
redistributing built packs.
