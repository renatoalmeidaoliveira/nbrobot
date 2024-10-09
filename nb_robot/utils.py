def process_suite(suite):
    tests = []
    for test in suite['tests']:
        test_data = {
            "name": test['name'],
            "doc": test.get('doc', ""),
            "status": test['status'],
            "elapsed_time": test['elapsed_time'],
            "start_time": test['start_time'],
            "body": process_body(test['body'])
        }
        tests.append(test_data)
    return tests

def process_body(body):
    results = []
    for item in body:
        body_type = item.get('type', None)
        inner_body = item.get('body', None)
        if body_type is None:
            if inner_body is None:
                result = {
                    "name": item['name'],
                    "args": item.get('args', []),
                    "status": item['status'],
                    "doc": item.get('doc', ""),
                    "elapsed_time": item['elapsed_time'],
                    "start_time": item['start_time'],
                }
                results.append(result)
            else:
                result = {
                    "name": item['name'],
                    "args": item.get('args', []),
                    "status": item['status'],
                    "doc": item.get('doc', ""),
                    "elapsed_time": item['elapsed_time'],
                    "start_time": item['start_time'],
                    "body": process_body(inner_body)
                }
                results.append(result)
    return results

