
def match_result(actual_result, expected_result):
  assert actual_result['status'] == expected_result['status'] and actual_result['result'] == expected_result['result']