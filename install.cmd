pyinstaller -F --noconsole ^
--add-binary controllers/actions.pyd;controllers ^
--add-binary controllers/ai.pyd;controllers ^
--add-binary controllers/base.pyd;controllers ^
--add-binary controllers/behaviors.pyd;controllers ^
--add-binary controllers/enemy.pyd;controllers ^
--add-binary controllers/player.pyd;controllers ^
--add-binary objects/base.pyd;objects ^
--add-binary objects/fleets.pyd;objects ^
--add-binary objects/other.pyd;objects ^
--add-binary objects/ships.pyd;objects ^
--add-binary objects/text.pyd;objects ^
--add-binary audio.pyd;. ^
--add-binary cell.pyd;. ^
--add-binary common.pyd;. ^
--add-binary constants.pyd;. ^
--add-binary loader.pyd;. ^
--add-binary menu.pyd;. ^
--add-binary processes.pyd;. ^
--add-binary speech.pyd;. ^
--add-binary Tolk.pyd;. ^
--hidden-import pygame ^
forts.pyw
