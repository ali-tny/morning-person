morning-person
==============

Scripts to run on my raspberry pi to handle recording, processing, and posting
content for [morning-person](http://morningperson.co.uk).

Ran via daily cronjob, and requires environment variables:
- `MORNING_PERSON_DB_PATH`: path to sqlite database holding song information
- `MORNING_PERSON_CREATE_ENDPOINT`: http endpoint for creating posts
- `MORNING_PERSON_REST_AUTH_TOKEN`: REST auth token for posting content

Todo:
- testing
- refactor `process_video`
