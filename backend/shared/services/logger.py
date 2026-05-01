import structlog
import logging
import sys
import os
import requests
import threading

def http_log_ingestor(logger, name, event_dict):
    """Send logs to remote log server asynchronously."""
    url = os.getenv('LOG_SERVER_URL')
    if url:
        def post_log():
            try:
                requests.post(f"{url}/ingest", json=event_dict, timeout=1)
            except:
                pass
        threading.Thread(target=post_log).start()
    return event_dict

def configure_logging():
    """Configure structured logging."""
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        http_log_ingestor,
        structlog.processors.JSONRenderer()
    ]
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Standard logging setup
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

def get_logger(name):
    """Get structured logger."""
    return structlog.get_logger(name)
