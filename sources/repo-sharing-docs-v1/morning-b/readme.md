# Morning reader

An Android app that replaces a morning scroll through Twitter and blogs with a
fixed-length reading session. It splits classic books into self-contained
passages of 5–15 minutes and mixes them with long blog posts and short videos.
When your daily time is used up, the session ends.

To set it up, open this repository in Claude Code or Codex and paste:

> Set up Morning reader on my Android phone by following `docs/setup.md`, and
> build packs for Middlemarch and Frankenstein. Ask me questions to clarify
> before you start.

## What you get

- **A finite feed.** The home screen offers today's options, such as a
  10-minute passage of *Middlemarch*, a 12-minute essay from a blog you follow
  and a 6-minute video on Mary Shelley. Each option shows its length and a
  one-line hook. You can start an option only if it fits in the time left
  (45 minutes a day by default). You can always finish the passage you're
  reading.
- **Books that work in short sittings.** Passages break at chapter and scene
  changes. Some passages are marked as good places to start reading cold, and
  those come with a short recap of what came before. Short stories and poems are
  never split.
- **Your blogs, filtered.** The phone checks your feeds every 12 hours and keeps
  only posts that take 5 minutes or more to read. You can import an OPML file
  from Feedly or another reader, or add feeds one by one.
- **Explain.** Select a word or passage and tap **Explain**. You get a definition
  or a short explanation, in the language of the book.
- **Reading time adjusts to you.** The app measures your reading speed, and
  passage lengths use that speed.
- **Any public-domain book.** Books come from
  [Project Gutenberg](https://www.gutenberg.org/), using the cleaner
  [Standard Ebooks](https://standardebooks.org/) edition when one exists.
  Languages other than English work: the author's shelf includes Spanish stories
  and poems.

## Cost and effort

- **Setup:** about an hour with a coding agent, by our estimate, most of it
  installing the Android build tools. You need a Mac, a phone
  with Android 12 or newer, an [OpenRouter](https://openrouter.ai/) key (paid;
  $5 of credit covers several books and months of daily use) and, for videos, a
  free [YouTube Data API](https://developers.google.com/youtube/v3/getting-started)
  key.
- **Adding a book:** about a minute and $0.02–0.65 in model calls, roughly $0.13
  per 100,000 words (measured on the author's eight-book shelf). Finding videos
  uses 500 of YouTube's 10,000 free daily quota units, so about 20 books a day
  can get videos.
- **Daily use:** each blog post hook costs about $0.003 and each Explain about
  $0.001, going by
  [OpenRouter's price](https://openrouter.ai/google/gemini-3.8-flash) of $0.75
  per million input tokens and $3.75 per million output tokens. That suggests
  about $1 a month for a heavy reader. This is an estimate, not a measurement.

## What's been tested

The author runs it on one phone (a Moto G35) and builds it on a Mac. Nobody else
has set it up yet, and it hasn't been tried on Windows or Linux. A fresh checkout
builds without API keys (checked 2026-09-29), but Explain and blog hooks need
the OpenRouter key.

## How it works

A Python script, `./pack`, runs on your computer. It downloads a book, asks
Gemini 3.8 Flash (through OpenRouter) to divide it into passages and write their
hooks and recaps, picks a few YouTube videos, and copies the result to the phone
over `adb`. The app, written in Kotlin with Jetpack Compose, does everything
else on the phone: it fetches blog feeds and calls the model for Explain and for
blog post hooks, so mornings don't depend on your computer. Your OpenRouter key
is compiled into the app, so keep the built APK to yourself.

## More

- [Setup](docs/setup.md): installing, building and adding books.
- [Book pack format](docs/book-pack.md): the JSON file the script writes and the
  app reads.
- [Decisions](DECISIONS.md): why the app works the way it does.
- The Literata font is under the SIL Open Font License
  ([licenses/literata-OFL.txt](licenses/literata-OFL.txt)).
