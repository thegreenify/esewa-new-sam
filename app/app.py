import json

# --- Mock Database ---
# In a real-world scenario, this data would be in a database like DynamoDB.
# We've expanded it to include houseId (HID).
MOCK_DATABASE = [
    {
        "employeeId": "E12345",
        "houseId": "H456",
        "allotteeName": "Rajesh Kumar",
        "aanId": "AAN98765",
        "mobile": "91-XXXXXX1234",
        "email": "rajesh.k@gov.in",
        "pan": "ABCDE1234F",
        "aadhaar": "XXXX-XXXX-1234",
        "dateOfAllotment": "2023-10-26",
        "employer": {
            "code": "MINDEF",
            "currentOffice": "Ministry of Defence, South Block, New Delhi"
        },
        "quarter": {
            "type": "Type-IV",
            "address": "123, Sector 4, R.K. Puram, New Delhi",
            "allottedTo": "Self",
            "ownedBy": "Directorate of Estate",
            "custodian": "CPWD, R.K. Puram Division"
        }
    },
    {
        "employeeId": "E67890",
        "houseId": "H789",
        "allotteeName": "Priya Singh",
        "aanId": "AAN54321",
        "mobile": "91-XXXXXX5678",
        "email": "priya.s@gov.in",
        "pan": "PQRST5678G",
        "aadhaar": "XXXX-XXXX-5678",
        "dateOfAllotment": "2022-05-15",
        "employer": {
            "code": "MOHA",
            "currentOffice": "Ministry of Home Affairs, North Block, New Delhi"
        },
        "quarter": {
            "type": "Type-V",
            "address": "456, Sector 13, R.K. Puram, New Delhi",
            "allottedTo": "Spouse",
            "ownedBy": "Departmental Pool",
            "custodian": "CPWD, R.K. Puram Division"
        }
    }
]

def lambda_handler(event, context):
    """
    Handles GET requests to /allottees/{id}
    - The {id} can be an employeeId or a houseId.
    - Supports field selection via the 'fields' query parameter.
    """
    print(f"Received event: {json.dumps(event)}")

    # 1. Get the identifier from the path
    lookup_id = event.get('pathParameters', {}).get('id')
    if not lookup_id:
        return {'statusCode': 400, 'body': json.dumps({'error': 'An ID (Employee ID or House ID) is required in the path.'})}

    # 2. Find the allottee by employeeId or houseId
    allottee_data = None
    for record in MOCK_DATABASE:
        if record.get('employeeId') == lookup_id or record.get('houseId') == lookup_id:
            allottee_data = record.copy()  # Use a copy to avoid modifying the original
            break

    if not allottee_data:
        return {'statusCode': 404, 'body': json.dumps({'error': 'Allottee not found', 'id': lookup_id})}

    # 3. Handle selective field projection
    query_params = event.get('queryStringParameters') or {}
    fields_to_return = query_params.get('fields')

    if fields_to_return:
        # Split comma-separated fields and strip any whitespace
        requested_fields = [field.strip() for field in fields_to_return.split(',')]
        
        # Create a new dictionary with only the requested fields
        projected_data = {}
        for field in requested_fields:
            if field in allottee_data:
                projected_data[field] = allottee_data[field]
        
        # If no valid fields were requested, return an error
        if not projected_data:
             return {'statusCode': 400, 'body': json.dumps({'error': 'None of the requested fields are valid.', 'requestedFields': requested_fields})}
        
        final_data = projected_data
    else:
        # If 'fields' param is not present, return the full object
        final_data = allottee_data
        
    # 4. Formulate the successful response
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(final_data)
    }
