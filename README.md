# mindfeed

Automatically create Beeminder datapoints for posts in RSS/Atom feeds.


## Requirements

- [Beeminder](https://www.beeminder.com/) account.
- [Beeminder authentication token](https://www.beeminder.com/api#auth)
- A destination Beeminder goal.
- [Heroku](https://www.heroku.com/) account.
- [Heroku toolbelt](https://toolbelt.heroku.com/).


## Configuration

    git clone git@github.com:zeckalpha/mindfeed.git
    cd mindfeed
    heroku apps:create <somename>-mindfeed
    heroku config:set BEEMINDER_API_URL="https://www.beeminder.com/api/v1/"
    heroku config:set USERNAME=<your-beeminder-username>
    heroku config:set AUTH_TOKEN =<your-beeminder-authentication-token>
    heroku config:set GOAL=<your-beeminder-goal-name>
    heroku config:set FEED_URL=<your-feed-url>
    git push heroku master
