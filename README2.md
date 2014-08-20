# Mindfeed

## Installation and Configuration

- Heroku toolbelt
- Heroku Postgres credentials
- S3 credentials
- Mailgun credentials

## Infrastructure

### db

- Feed (Subscription)
- Entry (Version)
- Feature (Type)
- User

- Postgres
- S3


### app

Hosts the following:

- user registration
- login view
- feed subscription management
- reports on feeds and entries
- status view


### worker

Fetches outdated feeds. For each outdated feed:

- update entries
- extract features
- send an email


### feature_extraction

- Number of words
- ...


# Some day

- app improvements:
    - informational website
    - a demo
- Error logging and reporting
- Add more feature extractors
- REST API (Sandman?)
- Re-integrate Beeminder
- Billing (Stripe)
    - Evaluate pricing models
- Spell check
- Style/diction-like suggestions
- Predictive feed fetching
- Google Analytics integration
- Old-style Technorati
- Foreign language support
- Mindfeed Analytics:
    - Likert scale + user tracking
    - embeddable like Disqus
- Quality model
    - http://grouplens.org/site-content/uploads/2013/09/wikisym2013_warnckewang-cosley-riedl.pdf
    - Build on top of extracted features
    - Evaluate model against:
        - hand scores
        - manually selected good entries
        - user behavior
    - Extend model with feed adaptation
