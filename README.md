# Grow Message Support Service

## Web-Hosted Application

[Grow AWS Hosted Service](http://54.161.208.77/)

1. Click the link above to go to the application
2. Enter username `admin` and password `password` to get in
3. Send a text message to 717-229-0088
4. Refresh/Navigate to Incoming Messages
5. The right most button should give you the option to respond, click it
6. Enter the response and send
7. Go to Outgoing Messages to confirm your response message is there


## Run Locally

1. Clone the repo, `cd` to the root, and run `docker-compose up`
2. In another terminal, ssh into backend and run the following scripts:
    - `./scripts/db-create.sh` (creates the 'grow' database)
    - `./scripts/db-migrate.sh` (runs migrations/creates tables)
    - `./scripts/create-admin-user.py` (allows you to create the admin user to log in locally)
3. Make sure you have `ngrok` installed, and run `ngrok http 80` to receive a tunnel to local host
4. Make sure you have a Twilio Account, and add the URL `{ngrok_tunnel}/twilio/incoming_sms` to the 
   incoming message callback and add `{ngrok_tunnel}/twilio/outgoing_sms_status` to the delivery status callback
5. Swap out the 3 Twilio related environment variables in the .env folder with your own
6. Run the demo as above with the web-hosted version
