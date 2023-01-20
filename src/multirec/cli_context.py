import click

from kedro.framework.session import KedroSession
from kedro.framework.project import settings
from kedro.config import ConfigLoader


class CliConfig(dict):
    def __init__(self, d, *args, **kwargs):
        click_ctx = click.get_current_context(silent=True)
        cli_args = click_ctx.params['params']

        for arg in cli_args:
            if arg in d:
                if 'filepath' in d[arg]:
                    d[arg]['filepath'] = cli_args[arg]
                else:
                    d[arg] = cli_args[arg]

        super().__init__(d, *args, **kwargs)


class CliConfigLoader(ConfigLoader):
    def get(self, *patterns: str) -> CliConfig:  # type: ignore
        return CliConfig(super().get(*patterns))



class CliSession(KedroSession):
    def _get_config_loader(self) -> ConfigLoader:
        """An instance of the config loader."""
        env = self.store.get("env")
        extra_params = self.store.get("extra_params")

        config_loader_class = CliConfigLoader
        return config_loader_class(
            conf_source=str(self._project_path / settings.CONF_SOURCE),
            env=env,
            runtime_params=extra_params,
            **settings.CONFIG_LOADER_ARGS,
        )
