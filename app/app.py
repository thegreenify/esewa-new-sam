import json

def lambda_handler(event, context):
    """
    This function handles GET requests to /allottees/{employeeId}
    """
    print(f"Received event: {json.dumps(event)}")

    # 1. Extract employeeId from the API Gateway path parameters
    try:
        employee_id = event.get('pathParameters', {}).get('employeeId')
        if not employee_id:
            raise ValueError("employeeId is required in path")
    except (AttributeError, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }

    # 2. Mock database lookup
    # In a real application, this would query a database like DynamoDB.
    mock_database = {
        "E12345": {
            "allotteeName": "Rajesh Kumar",
            "employeeId": "E12345",
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
        }
    }

    allottee_data = mock_database.get(employee_id)

    # 3. Formulate the HTTP response
    if allottee_data:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(allottee_data)
        }
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Allottee not found', 'employeeId': employee_id})
        }
