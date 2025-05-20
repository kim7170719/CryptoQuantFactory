from utils.logging.error_reporter import ErrorReporter

def test_log_error():
    try:
        1/0
    except Exception as e:
        ErrorReporter.log_error(e, context='test_log_error')
        with open('logs/error.log', encoding='utf-8') as f:
            content = f.read()
        assert 'test_log_error' in content
        assert 'ZeroDivisionError' in content
