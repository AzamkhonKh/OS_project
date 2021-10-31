# OS_project
make project of client server 

https://www.dropbox.com/s/hjzyzkwye4oh5vr/OS_TTPU_project_AY_2021_22.pdf?dl=0
# How to run program
to get how we can interact with program and see available commands

install typer with pip

`pip install typer`

`python3 main.py --help`

#### to run server

`python3 main.py start-server`

#### to run clinet or interact with it

`python3 main.py start-client-test {username}`

for example:
`python3 main.py start-client-test azamhon`

to get detailed information:  
`python3 main.py start-client-test --help`

after connnection client it can write some commands and server may serve it after command "**exit**" it closes the server connection

# How it works

well i tried to use SOLID patter make simpler to manage code, now see that kind of overengineered here.

client and server talks to each other with json style:
{

    "command" : name of command,

    "message" : comment for client to make more user friendly interface

    "data": json data that depends on command value
}

made additional commands for users like 

**LOCAL_LS** -- to see what file they can write and readed before

I did not noticed any kind of racing conditions when used commands write and read
(on test made 4 client in localhost)

Did not tested on network depends on ip might be problems
