from datetime import timedelta, datetime

from finam.export import Exporter, Market, Timeframe

from . import SBER, SHARES_SESSION_MINUTES


class TestIntegration(object):

    def test_basic_but_ticks(self):
        exporter = Exporter()
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2016, 1, 1)

        got_daily = exporter.download(SBER.id, Market.SHARES,
                                      start_date=start_date,
                                      end_date=end_date,
                                      timeframe=Timeframe.DAILY)
        daily_count = len(got_daily)
        assert daily_count > 0

        got_minutes = exporter.download(SBER.id, Market.SHARES,
                                        start_date=start_date,
                                        end_date=end_date,
                                        timeframe=Timeframe.MINUTES30)
        minutes30_count = len(got_minutes)
        assert minutes30_count > daily_count * SHARES_SESSION_MINUTES / 30

        for got in (got_daily, got_minutes):
            assert got['<DATE>'].min() >= 20150101
            assert got['<DATE>'].max() <= 20160101
            assert '<LAST>' not in got.columns
            assert '<CLOSE>' in got.columns

    def test_ticks(self):
        exporter = Exporter()
        ticks_date = datetime(2016, 10, 27)
        got = exporter.download(SBER.id, Market.SHARES,
                                start_date=ticks_date,
                                end_date=ticks_date,
                                timeframe=Timeframe.TICKS)
        assert len(got) > SHARES_SESSION_MINUTES * 60
        assert got['<DATE>'].min() >= 20161027
        assert got['<DATE>'].max() < 20161027 + 1
        assert '<LAST>' in got.columns
        assert '<CLOSE>' not in got.columns
