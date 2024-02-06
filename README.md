This app uses aws bedrock to answer queries:

Prerequisites: aws cli configure, serverless npm framework installed

Run below commands to deploy:

`npm i`
`sls deploy`

To test:

`sls invoke -f api -d '{"body":"{\"prompt\":\"Tell me a joke.\"}"}'`