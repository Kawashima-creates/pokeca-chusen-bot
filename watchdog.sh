#!/bin/sh
# pokeca-bot 見張り役: ハートビートが一定時間更新されなければBotを再起動する。
# 「プロセスは生きてるが固まってオフライン」状態を検知して蘇生する。
HB="/Users/kawashima/pokeca-chusen-bot/bot_heartbeat"
STALE=240   # 秒。ハートビートがこれ以上古ければ異常とみなす

# ハートビートが無い＝起動直後等の可能性。何もしない（launchdが起動を担当）
[ -f "$HB" ] || exit 0

now=$(date +%s)
last=$(cat "$HB" 2>/dev/null || echo 0)
age=$((now - last))

if [ "$age" -gt "$STALE" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') heartbeat ${age}s古い→Bot再起動" >> /Users/kawashima/pokeca-chusen-bot/watchdog.log
    launchctl kickstart -k gui/501/com.kawashima.pokeca-bot
fi
