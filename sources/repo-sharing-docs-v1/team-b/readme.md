# Team agent server

A private server your organisation runs that gives each staff member a read-only copy of their own Gmail, Calendar, Tasks and Drive as ordinary files, so Claude Code or Codex can analyse their whole work history at once instead of a few items per request. It suits organisations of 10–50 people on Google Workspace with Macs, and costs about $116 a month for up to 20 people.

A typical request from a member:

> I suspect clients who raised budget concerns in their first call were the ones who later stopped working with us. Check that across my call transcripts and follow-up emails, and show me a few examples of how you judged "budget concerns". Ask me questions to clarify before you start.

## What it does for you

**For members (your staff):**

- **Analyses across everything, not one lookup at a time.** Connectors in Claude or ChatGPT fetch a handful of emails or documents per request. Here every email, calendar entry and Drive file is on disk, so the agent can search, script and classify thousands of items. One pilot member's Drive came to 2,534 items.
- **Long jobs keep running after they close the laptop.** Sessions and background jobs run on the server, and the agent reports back when a job finishes.
- **They keep the tools they know.** Members connect the Claude or Codex desktop app to the server, or use either from Terminal, with their existing Claude or ChatGPT plan and connectors. Shared Drive folders, Google Takeout archives and, optionally, Salesforce, Airtable and web search can be added.

**For whoever is responsible for the data:**

- **The data stays on one server you own.** Member homes sit on an encrypted volume, each member has their own Linux account, and no member can read another's files or see their processes. Nothing is copied to members' laptops.
- **Access to Google is read-only, and deletions propagate.** The monthly refresh replaces the previous copy, so anything deleted at the source leaves the server within a month. Offboarding means revoking Google access and deleting the account.
- **Server owners are the only administrators**, and can read all member data. The [overview for server owners](docs/owners-overview.md#access) explains why and what follows.

## Cost and effort

**Running costs** (DigitalOcean, [September 2026 prices](https://www.digitalocean.com/pricing/droplets)):

| Team size | Server | Encrypted storage ([$0.10/GB](https://docs.digitalocean.com/products/volumes/details/pricing/)) | Total per month |
|---|---|---|---|
| Up to ~20 members | Basic, 8 vCPU / 16 GB: $96 | 200 GB: $20 | ~$116 |
| Up to ~50 members | General Purpose, 8 vCPU / 32 GB: $252 | 500 GB: $50 | ~$302 |

Each open agent session uses 1–2 GB of memory, so size the server for how many people work at the same time, not for headcount; it can be resized later. On top of this come the Claude or ChatGPT plans members already use, and any [optional add-ons](docs/owners-overview.md#optional-add-ons): backups from about $5 a month, web search at about $0.007 per search.

**Server owners: an afternoon to set up, then about ten minutes per member.** You create a DigitalOcean server with an encrypted volume, run the install and hardening scripts, create an internal Google OAuth app with read-only scopes, and add each member with one script. In the pilot, Claude Code did all of this through browser control; a person stepped in only to sign in to accounts, grant access and enter payment details. To do the same, give your agent this prompt from a clone of this repository:

> Set up this team agent server by following docs/owners-setup.md. Pause when you need me to sign in, approve access or enter payment details. Ask me questions to clarify before you start, including the region, server size and timezone.

Ongoing work is a monthly look at the metadata report and disk space.

**Members: about 15 minutes, in one sitting.** Server owners share a key and a setup command through a password manager. The member pastes the command into Terminal, adds the server in their Claude or Codex app, and signs in to Google when the agent asks.

## What was tested

A one-member pilot on DigitalOcean in September 2026 ran the Gmail, Calendar, Tasks and Drive imports, including a folder shared by someone else, the monthly refresh, the host hardening (also after a reboot) and the Google sign-in with a Workspace account. Among the add-ons, backups were tested against a local target, web search with a test key, and Airtable on a test base.

Untested: more than one member at a time on a real server (isolation between members is checked by a script, not by a pilot with several people), shared drives, Salesforce (automated tests only) and backups to DigitalOcean Spaces. Slack sign-in isn't built yet. The [overview](docs/owners-overview.md#what-it-is) has details.

## How it works

The server runs Ubuntu on DigitalOcean with `/home` on an encrypted volume. Each member has a Linux account reachable only by SSH key. A Python command, `workspace-import`, signs the member in to Google with their own consent, downloads each source into a new copy under `~/workspace/data`, records a hash of every file so the copy can be verified, and then replaces the previous copy; a refresh that returns far fewer records than last time stops instead. A monthly timer runs the refresh as the member. Members' agents read an `AGENTS.md` in their home that explains the layout and commands, and save their own work in `~/workspace/work`, which refreshes never touch.

## Documents

- [Overview for server owners](docs/owners-overview.md): what gets installed, what it means for privacy, the optional add-ons, and the decisions to make.
- [Setup steps](docs/owners-setup.md): server setup, adding and removing members, maintenance.
- [Member guide](docs/member-guide.md): the one-time setup and everyday use, to send to members after filling in `[OWNERS_CONTACT]`.
- [What the server can and can't do](docs/capabilities.md), for members and for deciding whether it fits your team.
- [Instructions for members' agents](docs/member-start.md), installed automatically as `AGENTS.md` and `CLAUDE.md` in every member's home.
