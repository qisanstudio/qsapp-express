# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from flask import jsonify
from flask.ext.restful import Resource, Api, reqparse
from express.blueprints import blueprint_apis

from express.models.account import AccountModel


account_parser = reqparse.RequestParser()
account_parser.add_argument(
    'uid', dest='uid',
    type=str, location='args',
    required=True, help='uid',
)


class AccountAPI(Resource):

    def get(self):
        args = account_parser.parse_args()
        account = AccountModel.query.get(args.uid)
        if account:
            return jsonify(account.as_dict())
        return jsonify({'code': 404})


api = Api(blueprint_apis)
api.add_resource(AccountAPI, '/account/')
