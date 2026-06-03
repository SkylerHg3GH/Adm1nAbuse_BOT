# Source of Adm1nAbuse BOT

Some parts are not sourced here. Do not ask why

## Not sourced

- config.yml
- bans.yml
- pdata.json
- bal.json
- queue.txt

## Up to date?

The last change was made on **6/2/2026**. 2 changes have been made in total.

## Where to host?

This bot was specifically made for the Minecraft server `adm1nabuse.net`

## How to use?

Download minescript from `minescript.net`, and put this repo into your `exec` folder, preferrably with something like `Bot\`<br>
Next, just do `Bot\bot` and you are done! You are now hosting an entire bot!<br>
**YOU MUST NOT USE THE SAME COMMAND PREFIX, THAT IS `!`.**

### Files that must be added
- config.yml
EXAMPLE CONFIG

```yml
qm:
  msgQueueInterval: 0.3
  warning: 5 # How long queue must be before it warns
messages:
  invalidExpressionMessage: "invalid expression :)"
bot:
  typoDetectionScoreCutoff: 70
```
- bans.yml
Format:
```yml
players:
  Someone:
    banned: true
    reason: "Bad people stay ban"
```
- pdata.json
Data: `{}`
- queue.txt
You do not need this, but its fine if you wanna add it. Just make sure it is empty.

