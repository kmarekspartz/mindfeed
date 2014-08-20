from mindfeed.email import delegation, MailDelegateInterface


class MailgunDelegate(MailDelegateInterface):
    pass


delegation.append(
    ({'MAILGUN_...'}, MailgunDelegate)
)
