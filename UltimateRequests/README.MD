all scripts refer to a workbench, which contains all the general configs and your credentials to login.

therefore you first need to initialize the environment using 
"python3 initWorkbench.py"
you can specify the location, where the creation script will place new challenges using e.g.
"python3 initWorkbench.py --dirWorkbench ~/challenges"
moreover you can define the workbench directory
"python3 initWorkbench.py --dirChallenge ~/.rzt"
or of course combine them, which I use in this readme
"python3 initWorkbench.py --dirWorkbench ~/.rzt --dirChallenge ~/challlenges"

having set up the workbench, you can create your first challenge.
This is done by the script createNewChallenge.
You need to pass the target url and a relative directory, in which the challenge files will be stored. This directory is a subtree to the general challenge directory.
python3 createNewChallenge.py --targetUrl "https://ringzer0team.com/challenges/1" --dirChallenge sql/injection/1

With the above config,t his creates the following directory
$HOME/challenges/web/xss1
the directory should contain the following files:
loginCheck.py
loginHandler.py
ManageRequest.py
request.config
requestHandler.py
staticMethods.py
__init__.py

To execute a request just run
"python3 ~/challenges/sql/injection/1ManageRequest.py"
it loads the config from the local request. config.
You can edit the request's behavior in the file requestHandler.py
The manage script will automatically login to ringzer0team before every script run, if neccessary. 
Otherwise it uses the session cookie from the last run

The requestHandler.py contains four methods, which define the behaviour of the request.
prepareRequest() can do client side stuff, like base64 encoding and prepare the request's content in general.
performRequest() executes the request
postProcessRequest() can analyze the response or extract only necessary information
run() defines the control flow of the above methods. You may iterate over the above methods tu execute multiple requests. This can be specified in run.


Troubleshooting:
you may have problem, when you try to copy your password, instead of typing it. If that's the case,
insert a random password as placeholder. The credentials are stored in $yourWorkBench/credentials.dat
Encode your password with base64 and replace the placeholder.
