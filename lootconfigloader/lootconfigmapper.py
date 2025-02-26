import os
from typing import List
from mobase import (
    IOrganizer,
    IPluginFileMapper,
    Mapping,
    PluginSetting,
    ReleaseType,
    VersionInfo,
)
from PyQt6.QtWidgets import QMainWindow


class LOOTConfigMapper(IPluginFileMapper):

    def __init__(self):
        super().__init__()

    def author(self) -> str:
        return "Parapets"

    def description(self) -> str:
        return "Allows for instance-specific LOOT configs"

    def init(self, organizer: "IOrganizer") -> bool:
        self.organizer = organizer
        organizer.onUserInterfaceInitialized(self.finish_init)
        return True

    def name(self) -> str:
        return "LOOT Config Loader"

    def settings(self) -> List["PluginSetting"]:
        return []

    def version(self) -> "VersionInfo":
        return VersionInfo(1, 0, 0, 0, ReleaseType.FINAL)

    def mappings(self) -> List["Mapping"]:
        mappings = []
        mappings.append(self.make_loot_mapping())

        return mappings

    def get_source_path(self) -> str:
        return os.path.join(self.organizer.basePath(), "LOOT Config Files")

    def get_destination_path(self) -> str:
        return os.path.join(os.environ["LOCALAPPDATA"], "LOOT")

    def make_loot_mapping(self) -> "Mapping":
        source = self.get_source_path()
        destination = self.get_destination_path()
        return Mapping(source,
                       destination,
                       is_directory=True,
                       create_target=False)

    def finish_init(self, window: QMainWindow) -> None:
        source = self.get_source_path()
        os.makedirs(source, exist_ok=True)

        destination = self.get_destination_path()
        game_name = self.organizer.managedGame().gameName()
        os.makedirs(os.path.join(destination, game_name), exist_ok=True)
