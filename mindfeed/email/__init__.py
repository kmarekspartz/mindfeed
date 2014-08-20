from mindfeed import config
from mindfeed.exc import NoDelegateError


delegation = []


class MailService(object):
    def __init__(self):
        for variables, delegate in delegation:
            all_variables_in_config = all([
                variable in config
                for variable in variables
            ])
            if all_variables_in_config:
                self.delegate = delegate()
                break
        else:
            raise NoDelegateError

    def send_fetch_report(self, feed_fetcher):
        self.delegate.bulk_send(
            feed_fetcher.report(),
            feed_fetcher.feed.subscriber_emails
        )


class MailDelegateInterface(object):
    def bulk_send(self, content, emails):
        raise NotImplementedError
