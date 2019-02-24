from .context import pandas_ta
from .data import sample_data, CORRELATION_THRESHOLD

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal

VERBOSE = False


class TestOverlap(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.open = cls.data['open']
        cls.high = cls.data['high']
        cls.low = cls.data['low']
        cls.close = cls.data['close']
        cls.volume = cls.data['volume']
        cls.correlation_threshold = CORRELATION_THRESHOLD

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        del cls.volume


    def setUp(self):
        self.overlap = pandas_ta.overlap

    def tearDown(self):
        del self.overlap
    

    def test_dema(self):
        dema = self.overlap.dema(self.close)
        self.assertIsInstance(dema, Series)
        self.assertEqual(dema.name, 'DEMA_10')

        try:
            tal_dema = tal.DEMA(self.close, 10)
            pdt.assert_series_equal(dema, tal_dema, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(dema, tal_dema)
            print(f"\nanalysis['corr']: {round(analysis['corr'], 3)}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"dema has low correlation: {analysis['corr']}")

    def test_ema(self):
        ema = self.overlap.ema(self.close, presma=False)
        self.assertIsInstance(ema, Series)
        self.assertEqual(ema.name, 'EMA_10')

        try:
            tal_ema = tal.EMA(self.close, 10)
            pdt.assert_series_equal(ema, tal_ema, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(ema, tal_ema)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"ema has low correlation: {analysis['corr']}")

    def test_fwma(self):
        fwma = self.overlap.fwma(self.close)
        self.assertIsInstance(fwma, Series)
        self.assertEqual(fwma.name, 'FWMA_10')

    def test_hl2(self):
        hl2 = self.overlap.hl2(self.high, self.low)
        self.assertIsInstance(hl2, Series)
        self.assertEqual(hl2.name, 'HL2')

    def test_hlc3(self):
        hlc3 = self.overlap.hlc3(self.high, self.low, self.close)
        self.assertIsInstance(hlc3, Series)
        self.assertEqual(hlc3.name, 'HLC3')

        try:
            tal_typicalprice = tal.TYPPRICE(self.high, self.low, self.close)
            pdt.assert_series_equal(hlc3, tal_typicalprice, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(hlc3, tal_typicalprice)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"hlc3/typicalprice has low correlation: {analysis['corr']}")

    def test_hma(self):
        hma = self.overlap.hma(self.close)
        self.assertIsInstance(hma, Series)
        self.assertEqual(hma.name, 'HMA_10')

    # @skip("close index requires Daily dates")
    def test_ichimoku(self):
        ichimoku = self.overlap.ichimoku(self.high, self.low, self.close)
        self.assertIsInstance(ichimoku, DataFrame)
        self.assertEqual(ichimoku.name, 'ICHIMOKU_9_26_52')

    def test_midpoint(self):
        # talib.MIDPOINT(timeperiod >= 2)
        midpoint = self.overlap.midpoint(self.close)
        self.assertIsInstance(midpoint, Series)
        self.assertEqual(midpoint.name, 'MIDPOINT_2')

        try:
            tal_midpoint = tal.MIDPOINT(self.close, 2)
            pdt.assert_series_equal(midpoint, tal_midpoint, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(midpoint, tal_midpoint)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"midpoint has low correlation: {analysis['corr']}")

    def test_midprice(self):
        # talib.MIDPRICE(timeperiod >= 2)
        midprice = self.overlap.midprice(self.high, self.low)
        self.assertIsInstance(midprice, Series)
        self.assertEqual(midprice.name, 'MIDPRICE_2')

        try:
            tal_midprice = tal.MIDPRICE(self.high, self.low, 2)
            pdt.assert_series_equal(midprice, tal_midprice, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(midprice, tal_midprice)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"midprice has low correlation: {analysis['corr']}")

    def test_ohlc4(self):
        ohlc4 = self.overlap.ohlc4(self.open, self.high, self.low, self.close)
        self.assertIsInstance(ohlc4, Series)
        self.assertEqual(ohlc4.name, 'OHLC4')

    def test_pwma(self):
        pwma = self.overlap.pwma(self.close)
        self.assertIsInstance(pwma, Series)
        self.assertEqual(pwma.name, 'PWMA_10')

    def test_rma(self):
        rma = self.overlap.rma(self.close)
        self.assertIsInstance(rma, Series)
        self.assertEqual(rma.name, 'RMA_10')

    def test_sma(self):
        sma = self.overlap.sma(self.close)
        self.assertIsInstance(sma, Series)
        self.assertEqual(sma.name, 'SMA_10')

        try:
            tal_sma = tal.SMA(self.close, 10)
            pdt.assert_series_equal(sma, tal_sma, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(sma, tal_sma)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"sma has low correlation: {analysis['corr']}")

    def test_t3(self):
        t3 = self.overlap.t3(self.close)
        self.assertIsInstance(t3, Series)
        self.assertEqual(t3.name, 'T3_10_0.7')

        try:
            tal_t3 = tal.T3(self.close, 10)
            pdt.assert_series_equal(t3, tal_t3, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(t3, tal_t3)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"t3 has low correlation: {analysis['corr']}")

    def test_tema(self):
        tema = self.overlap.tema(self.close)
        self.assertIsInstance(tema, Series)
        self.assertEqual(tema.name, 'TEMA_10')

        try:
            tal_tema = tal.TEMA(self.close, 10)
            pdt.assert_series_equal(tema, tal_tema, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(tema, tal_tema)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"tema has low correlation: {analysis['corr']}")

    def test_trima(self):
        trima = self.overlap.trima(self.close)
        self.assertIsInstance(trima, Series)
        self.assertEqual(trima.name, 'TRIMA_10')

        try:
            tal_trima = tal.TRIMA(self.close, 10)
            pdt.assert_series_equal(trima, tal_trima, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(trima, tal_trima)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"trima has low correlation: {analysis['corr']}")

    def test_vwap(self):
        vwap = self.overlap.vwap(self.high, self.low, self.close, self.volume)
        self.assertIsInstance(vwap, Series)
        self.assertEqual(vwap.name, 'VWAP')

    def test_vwma(self):
        vwma = self.overlap.vwma(self.close, self.volume)
        self.assertIsInstance(vwma, Series)
        self.assertEqual(vwma.name, 'VWMA_10')

    def test_wma(self):
        wma = self.overlap.wma(self.close)
        self.assertIsInstance(wma, Series)
        self.assertEqual(wma.name, 'WMA_10')

        try:
            tal_wma = tal.WMA(self.close, 10)
            pdt.assert_series_equal(wma, tal_wma, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(wma, tal_wma)
            print(f"\nanalysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"wma has low correlation: {analysis['corr']}")
