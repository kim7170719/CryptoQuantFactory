from backtest.event_engine import EventEngine

def test_event_engine():
    engine = EventEngine()
    def event(data):
        data['event'] = 1
        return data
    import pandas as pd
    data = pd.DataFrame({'a': [1,2,3]})
    engine.add_event(event)
    result = engine.process(data)
    assert 'event' in result
