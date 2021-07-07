"""
API definitions.
"""

from flask_restful import Resource, reqparse
from os import getcwd

cwd = os.getcwd()

# API LAYOUT
#   Open endpoints for 3 functionalities
#       url/api/auth retrieves auth tokens
#       url/api/log logs user into session logs
#       url/api/email emails session logs to session admin

class Email(Resource):
    def get(self):
        # will do something not sure yet
        print('GET AT YE, EMAIL!')
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('destemail', required=True)
        parser.add_argument('sessionid', required=True)
        
        # args = parser.parse_args()

        # here we will implement GMAIL API to use official account
        # of service to email logs to requestor
        
        # return will most likely be return code of GMAIL API
        return {'message': 'SUCCESS'}, 200
    pass


class Log(Resource):
    def get(self):
        # extend to allow for accessing logs based on session hash
        print('GET AT YE, LOGS!')
        
        parser = reqparse.RequestParser()

        parser.add_argument('sessionid', required=True)
        args = parser.parse_args()
        
        sessionid = args['sessionid']

        # ok, ok, check existence of filename <sessionid>.csv before opening
        if not os.path.isfile(f'{cwd}/{sessionid}.csv'):
            return {'message': 'FAILURE'}, 404

        logs = pd.read_csv(f'{args[sessionid]}')
        return {'message': 'SUCCESS', 'logs': logs.to_dict()}, 200

    def post(self):
        parser = reqparse.RequestParser()   # need query parser
        
        # a POST will require some checks to log users into a session:
        parser.add_argument('asurite', required=True)       # ASURITE
        parser.add_argument('asuemail', required=True)      # ASU email
        parser.add_argument('fname', required=True)         # first name
        parser.add_argument('lname', required=True)         # last name
        parser.add_argument('sessionid', required=True)     # session id
        
        args = parser.parse_args()          # create dict from args
        # prepare CSV log entry for writing
        new_user_log_entry = pd.DataFrame({
            'asurite': [args['asurite']],
            'asuemail': [args['asuemail']],
            'fname': [args['fname']],
            'lname': [args['lname']]
            })
        sessionid = args['sessionid']
        
        # if current session does not have a logfile touch it
        if not os.path.exists(f'{cwd}/{sessionid}.csv'):
            with open(f'{cwd}/{sessionid}.csv', 'w') as f:
                f.write('')
                f.close()
        
        # we write the user information to log titled <session hash>.csv
        logs = pd.read_csv(f'{sessionid}.csv')
        # append new user log entry
        logs = logs.append(new_user_log_entry, ignore_index=True)
        # finalize log and write to disk
        logs.to_csv(f'{sessionid}.csv')
        return {'message': 'SUCCESS'}, 200  # send back success and HTTP CODE 200 OK
    pass
