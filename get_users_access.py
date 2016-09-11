"""
Imports the aws client to connect to aws
json module to print the dictionary in a valid json string
sys and getopt to parse command line arguments
"""
import boto3
import json
import sys, getopt

#Gets arguments from command line to be used in the AWS connections
auth_key_id = ""
auth_access_key = ""

try:
    myopts, args = getopt.getopt(sys.argv[1:],"a:s:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -a aws_access_key_id -s aws_secret_access_key" % sys.argv[0])
    sys.exit(2)

for options, arguments in myopts:
    if options == '-a':
        auth_key_id = arguments
    elif options == '-s':
        auth_access_key = arguments

#Connects to the IAM AWS client with provided credentials or with default ones if no credentials have been provided

if auth_key_id and auth_access_key:
    client = boto3.client(
        'iam',
        aws_access_key_id=auth_key_id,
        aws_secret_access_key=auth_access_key)
else:
    client = boto3.client(
        'iam'
        )

#Dictionary used to store the users and access keys
user_keys_dict = {}

"""
Uses the IAM connection to list the users.
A temporary list to store the access key is created for the user in the current loop.
For each of the users, the code will assign the user name to a variable, for easier readibility and then query the access keys for it.
Each of the access keys for the user is then added to the temporary access keys list.
The list is added to the user_keys_dict dictionary that uses the user name as the key, and the list of access keys as the value for that key.
"""
try:
    for user in client.list_users()['Users']:
        user_name = user['UserName']
        user_access_key_list = []
        for access_key in client.list_access_keys(UserName=user_name)['AccessKeyMetadata']:
            user_access_key_list.append(access_key['AccessKeyId'])
        user_keys_dict[user_name] = user_access_key_list
except Exception, e:
    print "There has been an error trying to get the user data, please check error message"
    print str(e)

print json.dumps(user_keys_dict)