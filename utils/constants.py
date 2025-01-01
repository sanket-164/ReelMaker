UPLOAD_DIR = "uploaded_videos"
AUDIO_DIR = "extracted_audios"
TEXT_DIR = "transcribed_texts"
REEL_DIR = "short_reels"

SIDE_NAV_HEADERS = [
    ":material/passkey: Login",
    ":material/person_edit: Register",
    ":material/person_alert: Forgot Password",
]

TOP_NAV_HEADERS = [
    "Reel It!",
    "Upload",
    "Generate Reel",
    "Saved Reels",
    "Account",
]

TOP_NAV_ICONS = ["camera-reels", "upload", "stars", "file-check", "person"]

RESOLUTIONS_STR = [
    "Portrait 240p",
    "Portrait 360p",
    "Portrait 480p",
    "Portrait 720p (HD)",
    "Portrait 1080p (Full HD)",
    "Landscape 240p",
    "Landscape 360p",
    "Landscape 480p",
    "Landscape 720p (HD)",
    "Landscape 1080p (Full HD)",
    "Square 240p",
    "Square 360p",
    "Square 480p",
    "Square 720p (HD)",
    "Square 1080p (Full HD)",
]

RESOLUTIONS_PIXEL = [
    [240, 426],  # 240p Portrait
    [360, 640],  # 360p Portrait
    [480, 854],  # 480p Portrait
    [720, 1280],  # 720p Portrait
    [1080, 1920],  # 1080p Portrait (Full HD vertical)
    [426, 240],  # 240p Landscape
    [640, 360],  # 360p Landscape
    [854, 480],  # 480p (Standard Definition)
    [1280, 720],  # 720p (HD)
    [1920, 1080],  # 1080p (Full HD)
    [240, 240],  # 240 × 240 (Square)
    [360, 360],  # 360 × 360 (Square)
    [480, 480],  # 480 × 480 (Square)
    [720, 720],  # 720 × 720 (Square)
    [1080, 1080],  # 1080 × 1080 (Square)
]
