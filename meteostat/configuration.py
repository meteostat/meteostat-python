import os
from dataclasses import dataclass
from typing import List, Optional

from meteostat.core.config import ConfigService


@dataclass
class Config(ConfigService):
    """
    Configuration
    """

    # Cache configuration
    cache_enable: bool = True
    cache_dir = os.path.expanduser("~") + os.sep + ".meteostat" + os.sep + "cache"
    cache_ttl: int = 60 * 60 * 24 * 30
    cache_autoclean: bool = True

    # Network configuration
    proxies: List = None

    # Provider configuration
    metno_user_agent: Optional[str] = None


config = Config()
