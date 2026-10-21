SERVICES = [
    {"slug": "spotify", "name": "Spotify", "category": "Музика", "color": "#1db954", "icon": "spotify", "price": "99", "keys": ["spotify"], "domain": "spotify.com"},
    {"slug": "apple-music", "name": "Apple Music", "category": "Музика", "color": "#fa3b55", "icon": "applemusic", "price": "99", "keys": ["applemusic"], "domain": "music.apple.com"},
    {"slug": "netflix", "name": "Netflix", "category": "Стрімінг", "color": "#e50914", "icon": "netflix", "price": "299", "keys": ["netflix"], "domain": "netflix.com"},
    {"slug": "youtube-premium", "name": "YouTube Premium", "category": "Стрімінг", "color": "#ff2d45", "icon": "youtube", "price": "159", "keys": ["youtube"], "domain": "youtube.com"},
    {"slug": "disney-plus", "name": "Disney+", "category": "Стрімінг", "color": "#3b66e0", "icon": "disney", "price": "199", "keys": ["disney"], "domain": "disneyplus.com"},
    {"slug": "max", "name": "Max", "category": "Стрімінг", "color": "#8a4dff", "icon": "max", "price": "199", "keys": ["hbo"], "exact": ["max"], "domain": "max.com"},
    {"slug": "apple-tv", "name": "Apple TV+", "category": "Стрімінг", "color": "#a3a3ad", "icon": "appletv", "price": "199", "keys": ["appletv"], "domain": "tv.apple.com"},
    {"slug": "prime-video", "name": "Amazon Prime Video", "category": "Стрімінг", "color": "#1ea9e1", "icon": "primevideo", "price": "199", "keys": ["primevideo", "amazonprime"], "domain": "primevideo.com"},
    {"slug": "megogo", "name": "Megogo", "category": "Стрімінг", "color": "#ff7a00", "icon": "megogo", "price": "149", "keys": ["megogo"], "domain": "megogo.net"},
    {"slug": "sweet-tv", "name": "Sweet.tv", "category": "Стрімінг", "color": "#ff3d6e", "icon": "sweettv", "price": "129", "keys": ["sweet"], "domain": "sweet.tv"},
    {"slug": "twitch", "name": "Twitch", "category": "Стрімінг", "color": "#9146ff", "icon": "twitch", "price": "150", "keys": ["twitch"], "domain": "twitch.tv"},
    {"slug": "onedrive", "name": "Microsoft OneDrive", "category": "Хмара", "color": "#2a8ff0", "icon": "onedrive", "price": "1990", "keys": ["onedrive"], "domain": "onedrive.live.com"},
    {"slug": "icloud", "name": "iCloud", "category": "Хмара", "color": "#4a90e2", "icon": "icloud", "price": "49", "keys": ["icloud"], "domain": "icloud.com"},
    {"slug": "google-one", "name": "Google One", "category": "Хмара", "color": "#4285f4", "icon": "googleone", "price": "59", "keys": ["googleone"], "domain": "one.google.com"},
    {"slug": "dropbox", "name": "Dropbox", "category": "Хмара", "color": "#3b82ff", "icon": "dropbox", "price": "400", "keys": ["dropbox"], "domain": "dropbox.com"},
    {"slug": "steam", "name": "Steam", "category": "Ігри", "color": "#5b86b0", "icon": "steam", "price": "", "keys": ["steam"], "domain": "store.steampowered.com"},
    {"slug": "xbox-game-pass", "name": "Xbox Game Pass", "category": "Ігри", "color": "#1aa31a", "icon": "xbox", "price": "349", "keys": ["xbox", "gamepass"], "domain": "xbox.com"},
    {"slug": "playstation-plus", "name": "PlayStation Plus", "category": "Ігри", "color": "#2f6be0", "icon": "playstation", "price": "349", "keys": ["playstation", "psplus"], "domain": "playstation.com"},
    {"slug": "chatgpt", "name": "ChatGPT", "category": "ШІ", "color": "#10a37f", "icon": "chatgpt", "price": "840", "keys": ["chatgpt", "openai"], "domain": "chatgpt.com"},
    {"slug": "github-copilot", "name": "GitHub Copilot", "category": "ШІ", "color": "#8957e5", "icon": "copilot", "price": "420", "keys": ["githubcopilot"], "exact": ["copilot"], "domain": "github.com"},
    {"slug": "microsoft-365", "name": "Microsoft 365", "category": "Софт", "color": "#e8501a", "icon": "microsoft365", "price": "2400", "keys": ["microsoft365", "office365"], "domain": "microsoft365.com"},
    {"slug": "adobe", "name": "Adobe Creative Cloud", "category": "Софт", "color": "#fa2d1e", "icon": "adobe", "price": "1100", "keys": ["adobe"], "domain": "creativecloud.adobe.com"},
    {"slug": "notion", "name": "Notion", "category": "Софт", "color": "#9aa0aa", "icon": "notion", "price": "420", "keys": ["notion"], "domain": "notion.so"},
    {"slug": "figma", "name": "Figma", "category": "Софт", "color": "#a259ff", "icon": "figma", "price": "600", "keys": ["figma"], "domain": "figma.com"},
    {"slug": "canva", "name": "Canva", "category": "Софт", "color": "#12bfd0", "icon": "canva", "price": "400", "keys": ["canva"], "domain": "canva.com"},
    {"slug": "telegram-premium", "name": "Telegram Premium", "category": "Софт", "color": "#2aabee", "icon": "telegram", "price": "200", "keys": ["telegram"], "domain": "telegram.org"},
    {"slug": "duolingo", "name": "Duolingo", "category": "Навчання", "color": "#58cc02", "icon": "duolingo", "price": "2300", "keys": ["duolingo"], "domain": "duolingo.com"},
    {"slug": "claude", "name": "Claude", "category": "ШІ", "color": "#d97757", "icon": "claude", "price": "830", "keys": ["claude"], "domain": "claude.ai"},
    {"slug": "gemini", "name": "Google Gemini", "category": "ШІ", "color": "#4f7cff", "icon": "gemini", "price": "800", "keys": ["gemini", "googleai"], "domain": "gemini.google.com"},
    {"slug": "perplexity", "name": "Perplexity", "category": "ШІ", "color": "#1f8a8a", "icon": "perplexity", "price": "840", "keys": ["perplexity"], "domain": "perplexity.ai"},
    {"slug": "midjourney", "name": "Midjourney", "category": "ШІ", "color": "#6b7a99", "icon": "midjourney", "price": "420", "keys": ["midjourney"], "domain": "midjourney.com"},
    {"slug": "cursor", "name": "Cursor", "category": "ШІ", "color": "#8a8a96", "icon": "cursor", "price": "840", "keys": ["cursor"], "domain": "cursor.com"},
    {"slug": "grok", "name": "Grok (SuperGrok)", "category": "ШІ", "color": "#9aa0aa", "icon": "grok", "price": "1260", "keys": ["grok"], "domain": "grok.com"},
    {"slug": "ms-copilot", "name": "Microsoft Copilot", "category": "ШІ", "color": "#2b7bd6", "icon": "mscopilot", "price": "840", "keys": ["microsoftcopilot", "copilotpro"], "domain": "copilot.microsoft.com"},
    {"slug": "mistral", "name": "Mistral Le Chat", "category": "ШІ", "color": "#f2740a", "icon": "mistral", "price": "630", "keys": ["mistral"], "domain": "chat.mistral.ai"},
    {"slug": "elevenlabs", "name": "ElevenLabs", "category": "ШІ", "color": "#8d8d99", "icon": "elevenlabs", "price": "210", "keys": ["elevenlabs"], "domain": "elevenlabs.io"},
    {"slug": "suno", "name": "Suno", "category": "ШІ", "color": "#e8456b", "icon": "suno", "price": "420", "keys": ["suno"], "domain": "suno.com"},
    {"slug": "runway", "name": "Runway", "category": "ШІ", "color": "#8c93a3", "icon": "runway", "price": "630", "keys": ["runway"], "domain": "runwayml.com"},
    {"slug": "notebooklm", "name": "NotebookLM", "category": "ШІ", "color": "#5b6cf0", "icon": "notebooklm", "price": "", "keys": ["notebooklm"], "domain": "notebooklm.google.com"},
    {"slug": "kyivstar-tv", "name": "Київстар ТБ", "category": "Стрімінг", "color": "#2a6fdb", "icon": "kyivstartv", "price": "150", "keys": ["kyivstartv", "київстартб"], "domain": "tv.kyivstar.ua"},
    {"slug": "vodafone-tv", "name": "Vodafone TV", "category": "Стрімінг", "color": "#d11a1a", "icon": "vodafonetv", "price": "129", "keys": ["vodafonetv", "водафонтв"], "domain": "vodafone.ua"},
    {"slug": "oll-tv", "name": "Oll.tv", "category": "Стрімінг", "color": "#7a5cff", "icon": "olltv", "price": "100", "keys": ["olltv", "оллтв"], "domain": "oll.tv"},
    {"slug": "kyivstar", "name": "Київстар", "category": "Зв'язок", "color": "#1d9bd7", "icon": "kyivstar", "price": "250", "keys": ["kyivstar", "київстар"], "domain": "kyivstar.ua"},
    {"slug": "vodafone", "name": "Vodafone", "category": "Зв'язок", "color": "#e60000", "icon": "vodafone", "price": "250", "keys": ["vodafone", "водафон"], "domain": "vodafone.ua"},
    {"slug": "lifecell", "name": "lifecell", "category": "Зв'язок", "color": "#f5c400", "icon": "lifecell", "price": "200", "keys": ["lifecell", "лайфселл"], "domain": "lifecell.ua"},
    {"slug": "volia", "name": "Воля", "category": "Інтернет", "color": "#e2202b", "icon": "volia", "price": "250", "keys": ["volia"], "exact": ["воля"], "domain": "volia.com"},
    {"slug": "datagroup", "name": "Датагруп", "category": "Інтернет", "color": "#1f5fbf", "icon": "datagroup", "price": "240", "keys": ["datagroup", "датагруп"], "domain": "datagroup.ua"},
    {"slug": "triolan", "name": "Тріолан", "category": "Інтернет", "color": "#18a058", "icon": "triolan", "price": "250", "keys": ["triolan", "тріолан"], "domain": "triolan.ua"},
    {"slug": "lanet", "name": "Ланет", "category": "Інтернет", "color": "#0e8bc4", "icon": "lanet", "price": "200", "keys": ["lanet", "ланет"], "domain": "lanet.ua"},
    {"slug": "ukrtelecom", "name": "Укртелеком", "category": "Інтернет", "color": "#0b6bcb", "icon": "ukrtelecom", "price": "200", "keys": ["ukrtelecom", "укртелеком"], "domain": "ukrtelecom.ua"},
]

BY_SLUG = {s["slug"]: s for s in SERVICES}


def get_service(slug):
    return BY_SLUG.get(slug)


def find_by_name(name):
    key = "".join(ch for ch in name.lower() if ch.isalnum())
    for service in SERVICES:
        if key in service.get("exact", []) or any(word in key for word in service["keys"]):
            return service
    return None


def categories():
    return list(dict.fromkeys(s["category"] for s in SERVICES))
