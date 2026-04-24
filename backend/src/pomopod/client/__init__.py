from pomopod.client.http import HttpPomopodClient
from pomopod.core import config as core_config

daemon_config = core_config.get_daemon_settings()
client = HttpPomopodClient(base_url=f"http://{daemon_config.host}:{daemon_config.port}")
