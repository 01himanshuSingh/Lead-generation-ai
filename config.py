import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    """Scalable configuration settings layer."""

    # API Keys
    ANTHROPIC_API_KEY: str
# AI Provider Settings

    AI_PROVIDER: str
    GEMINI_API_KEY: str
    OPENAI_API_KEY: str
    # Proxy Settings
    PROXY_HOST: str
    PROXY_PORT: int
    PROXY_USER: str
    PROXY_PASS: str
    PROXY_TIMEOUT: int
    USE_FREE_FALLBACK_PROXIES: bool

    # General Settings
    TARGET_URL: str
    OUTPUT_PATH: str

    # Scraper Settings
    MAX_RETRIES: int
    HEADLESS: bool
    LOG_LEVEL: str

    @classmethod
    def load(cls) -> "Settings":

        def to_bool(val: str, default: str = "false") -> bool:
            return str(os.getenv(val, default)).lower() in ("1", "true", "yes", "y", "t")

        return cls(
             AI_PROVIDER=os.getenv(
        "AI_PROVIDER",
        "gemini",
    ),

    GEMINI_API_KEY=os.getenv(
        "GEMINI_API_KEY",
        "",
    ),
  OPENAI_API_KEY=os.getenv(
        "OPENAI_API_KEY",
        "",
    ),
            ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY", "dummy_anthropic_key"),
            PROXY_HOST=os.getenv("PROXY_HOST", "p.webshare.io"),
            PROXY_PORT=int(os.getenv("PROXY_PORT", "80")),
            PROXY_USER=os.getenv("PROXY_USER", "dummy"),
            PROXY_PASS=os.getenv("PROXY_PASS", "dummy"),
            PROXY_TIMEOUT=int(os.getenv("PROXY_TIMEOUT", "10")),
            USE_FREE_FALLBACK_PROXIES=to_bool("USE_FREE_FALLBACK_PROXIES", "false"),
            TARGET_URL=os.getenv("TARGET_URL", "https://example.com"),
            OUTPUT_PATH=os.getenv("OUTPUT_PATH", "data/output.xlsx"),
            MAX_RETRIES=int(os.getenv("MAX_RETRIES", "3")),
            HEADLESS=to_bool("HEADLESS", "true"),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO").upper(),
        )

settings = Settings.load()