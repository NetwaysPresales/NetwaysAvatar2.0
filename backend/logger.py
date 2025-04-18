import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("proxy_server.log"),
    ]
)

logger = logging.getLogger(__name__)

logger.disabled = False