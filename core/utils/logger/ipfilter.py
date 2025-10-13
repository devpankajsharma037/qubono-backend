import logging

class RequestIPFilter(logging.Filter):
    def filter(self, record):
        try:
            from core.utils.logger.logger_ip_middleware import get_current_ip
            record.ip = get_current_ip()
        except Exception:
            record.ip = 'NA'
        return True
