# Signals subpackage

## Decisions to take (@twopirllc I let this section decide to you)

- [ ] Split subpackage between signals/events and periods/areas or to have only one subpackage
- [ ] Name of subpackage(s)
- [ ] For each signal can we have two kind of outputs? (crossing signals and periods/areas). If so, do we want to split the indicator in two functions, have a parameter to change from one to another or always output both of them?
- [ ] General naming of indicators created in this subpackage (for example mark 'XA'/'XB' for crossing above/below and 'A'/'B' for periods above/below or more splicit naming that describe bearish/bullish signals)

## Signals to be added

- [x] RSI (Overbought/oversold 80/20)
- [ ] Extended RSI (Overbought/oversold 80/20 and positive trend when $RSI_t$ > $RSI_{t-1}$)
- [ ] Crossing EMA(50) and EMA(200) (long term bearish/bullish signal)
- [ ] Crossing EMA(12) and EMA(26) (short term bearish/bullish signal)
- [ ] Crossing MACD(26,12, 9) with 0 line (bearish/bullish signal)
- [ ] Stochastic oscillator (Overbough/oversold 80/20)
- [ ] Crossing Bollinger bands with close price
- [ ] Average directional index (ADX) cross with 25 (strong trend/drift)
