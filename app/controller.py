from boto3 import resource
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.environ.get('REGION_NAME')

resource = resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME
)

def create_table_cart():    
    table = resource.create_table(
        TableName = 'Cart', # Name of the table 
        KeySchema = [
            {
                'AttributeName': 'id',
                'KeyType'      : 'HASH' # HASH = partition key, RANGE = sort key
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'id', # Name of the attribute
                'AttributeType': 'S'   # N = Number (S = String, B= Binary)
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits'  : 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()
    return table

CartTable = resource.Table('Cart')

# add a new cart 
def write_to_cart_table(id, attributes:dict):
    #if id in CartTable, update products
    #if not, add new item 

    response = CartTable.put_item(
        Item = {
            'id'     : id,
            'products'  : [attributes],
        }
    )
    return response

# get a cart 
def read_from_cart_table(id):
    response = CartTable.get_item(
        Key = {
            'id'     : id
        },
        AttributesToGet = [
            'products' # valid types dont throw error, 
        ]                      # Other types should be converted to python type before sending as json response
    )
    return response

# update attribute within a specific cart (add another set of attributes to products)
# def add_to_cart(id, product:dict):
#     response = CartTable.update_item(
#         Key = {
#             'id': id
#         },
#         AttributeUpdates={
#             'products': {
#                 'Value'  : product['title'],
#                 'Action' : 'PUT' # # available options = DELETE(delete), PUT(set/update), ADD(increment)
#             }
#         },
#         ReturnValues = "UPDATED_NEW"  # returns the new updated values
#     )
#     return response

# remove product within a specific cart 
# def update_in_movie(id, data:dict):
#     response = CartTable.update_item(
#         Key = {
#             'id': id
#         },
#         AttributeUpdates={
#             'title': {
#                 'Value'  : data['title'],
#                 'Action' : 'PUT' # # available options = DELETE(delete), PUT(set/update), ADD(increment)
#             },
#             'director': {
#                 'Value'  : data['director'],
#                 'Action' : 'PUT'
#             }
#         },
#         ReturnValues = "UPDATED_NEW"  # returns the new updated values
#     )
#     return response

