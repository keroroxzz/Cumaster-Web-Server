# Cumaster Heroku Server

This is the source code of the Cumaster Heroku server I made a few years ago for fun.

Cumaster is a Gomoku-like Go game my friends and I invented. It's more complex and funnier to play.

To promote this novel game, I wrote this project to enable network gaming worldwide. However, it didn't make a hit. So I opensource the project here to enable anyone who is interested in this game to hold their game server.

# Installation

Please follow the official steps to hold a Heroku server locally.

Also, set the PostgreSQL database locally and fill in the information in cumaster/settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql', 
            'NAME': 'name of the database', 
            'USER': 'username', 
            'PASSWORD': 'password', 
            'HOST': 'localhost',
            'PORT': 'port'
        }
    }

You may also need to set up the SECRET_KEY in cumaster/settings.py.

# License

MIT License only applies to source code. We reserve all rights to the game itself. But we allow and encourage any kind of non-commercial application and re-distribution to the game itself.