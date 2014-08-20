from mindfeed.email import delegation, MailDelegateInterface


class SmtpDelegate(MailDelegateInterface):
    pass


delegation.append(
    ({'SMTP_...'}, SmtpDelegate)
)
