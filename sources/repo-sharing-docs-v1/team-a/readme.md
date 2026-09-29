# Team agent server

A private server that gives each person in your organisation a read-only copy of their own work data (Gmail, Calendar, Tasks and Drive, plus shared folders and optional Salesforce or Airtable) as ordinary files. They analyse it with Claude Code or Codex running on the server instead of on their laptop. It's built for organisations of 10–50 people on Google Workspace whose staff use Macs, and it runs on one DigitalOcean server for about $116–$302 a month.

Example of what a member can ask:

> I suspect clients who raised budget concerns in their first call were the ones who later stopped working with us. Check that across my call transcripts and follow-up emails, and show me a few examples of how you judged "budget concerns". Ask me questions to clarify before you start.

## What it gives your team

1. **Analysis across the whole history, not one lookup at a time.** Connectors in Claude or ChatGPT fetch a handful of emails or documents per request. Here the agent has every email, calendar entry and Drive file on disk, so it can search, script and classify thousands of items with ordinary tools (`rg`, `sqlite3`, Python). In the pilot, one person's Drive came to 2,534 items.
2. **Jobs that keep running when the laptop closes.** Members connect the Claude or Codex desktop app to the server over SSH, or use Claude Code or Codex from Terminal. Sessions and long background jobs run on the server, and no data is copied to members' machines.
3. **Data kept in one place you control.** The copies sit on an encrypted volume on a server your organisation owns, with one Linux account per member, so members can't read each other's files. Google access is read-only. Each monthly refresh replaces the previous copy, so anything deleted at the source leaves the server within a month.

## Check it fits before you start

You need:

- **Google Workspace**, with someone who can create an Internal OAuth app in your Google Cloud organisation and, if your API controls restrict third-party apps, mark it as Trusted.
- **A Claude or ChatGPT plan for the organisation.** Whatever the agent reads is sent to Anthropic or OpenAI under that plan's terms.
- **Members on Macs.** The member guide is written for macOS; the server itself only needs SSH.
- **One or two server owners** comfortable running commands in a terminal. They create accounts, hold the credentials and do a short monthly check.
- **A DigitalOcean account.** The setup scripts rely on DigitalOcean's encrypted volumes and first-boot scripts. Other providers haven't been tried; the parts to change would be [`infra/bootstrap.sh`](infra/bootstrap.sh), the volume path in [`infra/setup-host.sh`](infra/setup-host.sh), and the optional backups to DigitalOcean Spaces.

Decide these trade-offs up front:

- **Server owners can read every member's data**, including the Google tokens the monthly refresh needs. Linux account separation doesn't hide anything from an administrator, so choose owners your staff would trust with their inboxes.
- **SSH is open to the internet on port 22**, with key-only login. An IP allow-list would lock out members who travel.
- **There are no backups by default.** Downloaded data can be fetched again, but members' own notes are lost with the server unless you add the [backup add-on](docs/owners-setup.md#backups-of-members-work) (about $5/month).

## How far it has been tested

A one-member pilot on DigitalOcean in September 2026 passed the Gmail, Calendar, Tasks and Drive imports, including a folder shared by someone else, the monthly refresh, the Google sign-in, and the host hardening, including after a reboot. The automated tests (`uv run pytest -q`) cover the importers and sign-in.

Not yet tried on a real server: several members using it at once, Google shared drives, Salesforce, and backups to DigitalOcean Spaces. Slack sign-in isn't built. The [overview for server owners](docs/owners-overview.md#what-it-is) has the full list.

## Cost and effort

**Running costs** (DigitalOcean [prices checked September 2026](https://www.digitalocean.com/pricing/droplets)):

| Team size | Server | Encrypted storage ([$0.10/GB](https://docs.digitalocean.com/products/volumes/details/pricing/)) | Total per month |
|---|---|---|---|
| Up to ~20 members | Basic, 8 vCPU / 16 GB: $96 | 200 GB: $20 | ~$116 |
| Up to ~50 members | General Purpose, 8 vCPU / 32 GB: $252 | 500 GB: $50 | ~$302 |

Each open agent session uses 1–2 GB of memory, so size the server for how many people work at once rather than headcount; it can be resized later. On top of this come the Claude or ChatGPT plans members already use and any [optional add-ons](docs/owners-overview.md#optional-add-ons), such as web and LinkedIn search at about $0.007 per search.

**Server owners: an afternoon, then about ten minutes per member.** The [setup steps](docs/owners-setup.md) are:

1. Create a DigitalOcean server with an encrypted volume, using the first-boot script in this repository.
2. Run two commands to install the software and harden the server: `/home` on the encrypted volume, SSH keys only, processes hidden between users, and automatic security updates with a 04:00 reboot when needed.
3. Create an internal Google OAuth app with read-only scopes and copy its file to the server.
4. Add each member with one script, and share their key through a password manager.

In the pilot, Claude Code carried out these steps by controlling a browser; a person only signed in to accounts, granted access and entered payment details.

**Members: about 15 minutes, in one sitting.** They paste one command into Terminal, add the server in their Claude or Codex app, and sign in to Google when the agent asks. Their first full download can take several hours and runs on the server.

**Ongoing:** a monthly look at disk space and a metadata report listing each member's sources and when they last refreshed. Offboarding means revoking the member's Google access and deleting their account.

## Documents

- [Overview for server owners](docs/owners-overview.md): what gets installed, what it means for privacy, and optional add-ons. Read this before deciding.
- [Setup steps](docs/owners-setup.md): server setup, adding and removing members, maintenance.
- [Member guide](docs/member-guide.md): one-time setup and everyday use. Replace the one placeholder, `[OWNERS_CONTACT]`, before sending it.
- [What the server can and can't do](docs/capabilities.md), written for members.
- [Instructions for members' agents](docs/member-start.md), installed as `AGENTS.md` and `CLAUDE.md` in every member's home so Claude and Codex load them automatically.

## Contents

| Path | Purpose |
|---|---|
| `workspace_import/` | The `workspace-import` command: Google sign-in, resumable imports, integrity checks, monthly refresh |
| `infra/` | First-boot script, host hardening, installer, member creation, Codex installer, scheduled jobs |
| `scripts/` | Deployment, host and member checks, metadata report for server owners |
| `config/slack-app-manifest.json` | Read-only Slack app definition, for when Slack sign-in is built |
| `tests/` | Automated tests: `uv sync --frozen && uv run pytest -q` |

Never commit credentials, exports or member data.
