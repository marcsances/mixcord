# mixcord
Integrate Mixcloud uploads with Discord via webhook

Yet another night hack. This is a script that polls new streams from Mixcloud API for a given user and updates a Discord webhook.

Absolutely most basic type of integration. No error handling. Use on your own.

## Configuration

Copy ``config.template.json`` into ``config.json`` and setup:

* ``messages.newshow``: Message to add before the webhook embeds
* ``targets[*].target``: URL to either a user or playlist in Mixcloud (https://mixcloud.com/user or https://mixcloud.com/user/playlists/playlist)
* ``targets[*].webhook``: URL for the Discord webhook that should be notified (create a channel on Discord > Edit channel > Integrations > New webhook > Copy Webhook URL)

## Does it work with other webhooks (slack etc)?

Technically yes but I haven't tested, the webhook client must support embeds using Discord format, otherwise it will be only PO_NEW_SHOW message.

## Running

First install the requirements:

```bash
python -m pip install -r requirements.txt
```

Then I guess you want to set up a cron job to run ``main.py`` every few minutes.