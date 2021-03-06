from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

import logging

from flexget import plugin
from flexget.event import event
from flexget.plugin import PluginWarning
from requests.exceptions import RequestException
from flexget.utils.requests import Session as RequestSession

requests = RequestSession(max_retries=3)

plugin_name = 'slack'

log = logging.getLogger(plugin_name)


class SlackNotifier(object):
    """
    Example:

      slack:
        web_hook_url: <string>
        [channel: <string>] (override channel, use "@username" or "#channel")
        [username: <string>] (override username)
        [icon_emoji: <string>] (override emoji icon

    """
    schema = {
        'type': 'object',
        'properties': {
            'web_hook_url': {'type': 'string'},
            'channel': {'type': 'string'},
            'username': {'type': 'string'},
            'icon_emoji': {'type': 'string'}
        },
        'required': ['web_hook_url'],
        'additionalProperties': False
    }

    def notify(self, title, message, config):
        """
        Send a Slack notification
        """
        notification = {'text': message, 'channel': config.get('channel'), 'username': config.get('username')}
        if config.get('icon_emoji'):
            notification['icon_emoji'] = ':%s:' % config['icon_emoji'].strip(':')

        try:
            requests.post(config['web_hook_url'], json=notification)
        except RequestException as e:
            raise PluginWarning(e.args[0])


@event('plugin.register')
def register_plugin():
    plugin.register(SlackNotifier, plugin_name, api_ver=2, interfaces=['notifiers'])
