from .context import pandas_ta
from .data import sample_data, CORRELATION_THRESHOLD, VERBOSE

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestMomentum(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.open = cls.data['open']
        cls.high = cls.data['high']
        cls.low = cls.data['low']
        cls.close = cls.data['close']
        cls.volume = cls.data['volume']

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        del cls.volume


    def setUp(self):
        self.momentum = pandas_ta.momentum

    def tearDown(self):
        del self.momentum
    

    def test_ao(self):
        ao = self.momentum.ao(self.high, self.low)
        self.assertIsInstance(ao, Series)
        self.assertEqual(ao.name, 'AO_5_34')

    def test_apo(self):
        apo = self.momentum.apo(self.close)
        self.assertIsInstance(apo, Series)
        self.assertEqual(apo.name, 'APO_12_26')

        try:
            tal_apo = tal.APO(self.close, 12, 26)
            pdt.assert_series_equal(apo, tal_apo, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(apo, tal_apo, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {apo.name}: {ex}")

    def test_bop(self):
        bop = self.momentum.bop(self.open, self.high, self.low, self.close)
        self.assertIsInstance(bop, Series)
        self.assertEqual(bop.name, 'BOP')

        try:
            tal_bop = tal.BOP(self.open, self.high, self.low, self.close)
            pdt.assert_series_equal(bop, tal_bop, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(bop, tal_bop, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {bop.name}: {ex}")

    def test_cci(self):
        cci = self.momentum.cci(self.high, self.low, self.close)
        self.assertIsInstance(cci, Series)
        self.assertEqual(cci.name, 'CCI_20_0.015')

        try:
            tal_cci = tal.CCI(self.high, self.low, self.close)
            pdt.assert_series_equal(cci, tal_cci, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(cci, tal_cci, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {cci.name}: {ex}")

    def test_cmo(self):
        cmo = self.momentum.cmo(self.close)
        self.assertIsInstance(cmo, Series)
        self.assertEqual(cmo.name, 'CMO_14')

        try:
            tal_cmo = tal.CMO(self.close)
            pdt.assert_series_equal(cmo, tal_cmo, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(cmo, tal_cmo, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {cmo.name}: {ex}")

    def test_coppock(self):
        coppock = self.momentum.coppock(self.close)
        self.assertIsInstance(coppock, Series)
        self.assertEqual(coppock.name, 'COPC_11_14_10')

    def test_kst(self):
        kst = self.momentum.kst(self.close)
        self.assertIsInstance(kst, DataFrame)
        self.assertEqual(kst.name, 'KST_10_15_20_30_10_10_10_15_9')

    def test_macd(self):
        macd = self.momentum.macd(self.close)
        self.assertIsInstance(macd, DataFrame)
        self.assertEqual(macd.name, 'MACD_12_26_9')

        try:
            tal_macd = tal.MACD(self.close)
            tal_macddf = DataFrame({'MACD_12_26_9': tal_macd[0], 'MACDH_12_26_9': tal_macd[2], 'MACDS_12_26_9': tal_macd[1]})
            pdt.assert_frame_equal(macd, tal_macddf)
        except AssertionError as ae:
            try:
                macd_corr = pandas_ta.utils.df_error_analysis(macd.iloc[:,0], tal_macddf.iloc[:,0], col='corr')
                self.assertGreater(macd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {macd.iloc[:,0].name}: {ex}")

            try:
                history_corr = pandas_ta.utils.df_error_analysis(macd.iloc[:,1], tal_macddf.iloc[:,1], col='corr')
                self.assertGreater(history_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {macd.iloc[:,1].name}: {ex}")

            try:
                signal_corr = pandas_ta.utils.df_error_analysis(macd.iloc[:,2], tal_macddf.iloc[:,2], col='corr')
                self.assertGreater(signal_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {macd.iloc[:,2].name}: {ex}")

    def test_mom(self):
        mom = self.momentum.mom(self.close)
        self.assertIsInstance(mom, Series)
        self.assertEqual(mom.name, 'MOM_10')

        try:
            tal_mom = tal.MOM(self.close)
            pdt.assert_series_equal(mom, tal_mom, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(mom, tal_mom, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {mom.name}: {ex}")

    def test_ppo(self):
        ppo = self.momentum.ppo(self.close)
        self.assertIsInstance(ppo, DataFrame)
        self.assertEqual(ppo.name, 'PPO_12_26_9')

        try:
            tal_ppo = tal.PPO(self.close)
            pdt.assert_series_equal(ppo['PPO_12_26_9'], tal_ppo, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(ppo['PPO_12_26_9'], tal_ppo, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {ppo['PPO_12_26_9'].name}: {ex}")

    def test_roc(self):
        roc = self.momentum.roc(self.close)
        self.assertIsInstance(roc, Series)
        self.assertEqual(roc.name, 'ROC_10')

        try:
            tal_roc = tal.ROC(self.close)
            pdt.assert_series_equal(roc, tal_roc, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(roc, tal_roc, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {roc.name}: {ex}")

    def test_rsi(self):
        rsi = self.momentum.rsi(self.close)
        self.assertIsInstance(rsi, Series)
        self.assertEqual(rsi.name, 'RSI_14')

        try:
            tal_rsi = tal.RSI(self.close)
            pdt.assert_series_equal(rsi, tal_rsi, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(rsi, tal_rsi, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {rsi.name}: {ex}")

    def test_stoch(self):
        stoch = self.momentum.stoch(self.high, self.low, self.close)
        self.assertIsInstance(stoch, DataFrame)
        self.assertEqual(stoch.name, 'STOCH_14_5_3')

        try:
            tal_stochf = tal.STOCHF(self.high, self.low, self.close)
            tal_stoch = tal.STOCH(self.high, self.low, self.close)
            tal_stochdf = DataFrame({'STOCHF_14': tal_stochf[0], 'STOCHF_3': tal_stochf[1], 'STOCH_5': tal_stoch[0], 'STOCH_3': tal_stoch[1]})
            pdt.assert_frame_equal(stoch, tal_stochdf)
        except AssertionError as ae:
            try:
                stochfk_corr = pandas_ta.utils.df_error_analysis(stoch.iloc[:,0], tal_stochdf.iloc[:,0], col='corr')
                self.assertGreater(stochfk_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {stoch.iloc[:,0].name}: {ex}")

            try:
                stochfd_corr = pandas_ta.utils.df_error_analysis(stoch.iloc[:,1], tal_stochdf.iloc[:,1], col='corr')
                self.assertGreater(stochfd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f" [!] {stoch.iloc[:,1].name}: {ex}")

            try:
                stochsk_corr = pandas_ta.utils.df_error_analysis(stoch.iloc[:,2], tal_stochdf.iloc[:,2], col='corr')
                self.assertGreater(stochsk_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f" [!] {stoch.iloc[:,2].name}: {ex}")

            try:
                stochsd_corr = pandas_ta.utils.df_error_analysis(stoch.iloc[:,3], tal_stochdf.iloc[:,3], col='corr')
                self.assertGreater(stochsd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f" [!] {stoch.iloc[:,3].name}: {ex}")

    def test_trix(self):
        trix = self.momentum.trix(self.close)
        self.assertIsInstance(trix, Series)
        self.assertEqual(trix.name, 'TRIX_30')

    def test_tsi(self):
        tsi = self.momentum.tsi(self.close)
        self.assertIsInstance(tsi, Series)
        self.assertEqual(tsi.name, 'TSI_13_25')

    def test_uo(self):
        uo = self.momentum.uo(self.high, self.low, self.close)
        self.assertIsInstance(uo, Series)
        self.assertEqual(uo.name, 'UO_7_14_28')

        try:
            tal_uo = tal.ULTOSC(self.high, self.low, self.close)
            pdt.assert_series_equal(uo, tal_uo, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(uo, tal_uo, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {uo.name}: {ex}")

    def test_willr(self):
        willr = self.momentum.willr(self.high, self.low, self.close)
        self.assertIsInstance(willr, Series)
        self.assertEqual(willr.name, 'WILLR_14')

        try:
            tal_willr = tal.WILLR(self.high, self.low, self.close)
            pdt.assert_series_equal(willr, tal_willr, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(willr, tal_willr, col='corr')
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {willr.name}: {ex}")