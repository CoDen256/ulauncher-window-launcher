from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.search.apps.AppDb import AppDb
import logging

from ulauncher.utils.desktop.reader import find_apps_cached

logger = logging.getLogger(__name__)
class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

        for app in find_apps_cached():
            AppDb.get_instance().put_app(app)
        logger.info(list(find_apps_cached()))


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument()
        logger.info(query)
        logger.info(list(AppDb.get_instance().get_records()))
        result_list = AppDb.get_instance().find(query)
        logger.info(result_list)
        items = []
        for app_result_item in result_list:
            items.append(ExtensionResultItem(icon='images/icon.png', # not PixBuf, okay?
                                                name=app_result_item.get_name(),
                                                description=app_result_item.get_description(None),
                                                on_enter=HideWindowAction()))
        return RenderResultListAction(items)

if __name__ == '__main__':
    logger.info("HELO ITS ME MARIO")
    DemoExtension().run()