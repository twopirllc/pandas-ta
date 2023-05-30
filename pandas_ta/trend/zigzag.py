from pandas import DataFrame, concat, merge


def zigzag(high, low, pivot_leg=5, price_deviation=10, retrace=False, last_extreme=False, **kwargs):
    def find_extremum(rolling, pivot_leg):
        extremum = rolling[(
                (rolling.diff() == 0).cumsum() - (rolling.diff() == 0).cumsum().shift(
            pivot_leg - 1) == (pivot_leg - 1)).shift(-int(pivot_leg / 2)).fillna(False)]
        return extremum

    def calculate_swings(high, low, pivot_leg):
        rolling_high = high.rolling(window=pivot_leg, center=True, min_periods=0).max()
        rolling_low = low.rolling(window=pivot_leg, center=True, min_periods=0).min()

        high_swings = find_extremum(rolling_high, pivot_leg)
        low_swings = find_extremum(rolling_low, pivot_leg)

        highs = DataFrame({'swing_value': high_swings, 'swing_type': 'high'})
        lows = DataFrame({'swing_value': low_swings, 'swing_type': 'low'})
        swings_high_low = concat([highs, lows]).sort_index()
        return swings_high_low

    def price_dev(swings, price_deviation):
        """
        This function should get swings data and will return the swings,
        which are below the price deviation threshold.
        This data may have some high/low swings together and sequential which is not desired.
        These bad data will be handled in other functions.
        """
        swings = swings[((swings['swing_value'].pct_change()).abs()) > price_deviation / 100]
        swings = swings.reset_index(drop=True)

        return swings

    def swing_seq_catch(swing_data):
        """
        This function should get swings data and will return the swings,
        with one column added named new_swing_type which will determine if there is a change in swing type,
        e.g. from high to low or vice versa.
        """
        new_swings = swing_data[(swing_data.swing_type.shift(1) == swing_data.swing_type) |
                                (swing_data.swing_type.shift(-1) == swing_data.swing_type)]
        if len(new_swings) > 0:
            swing_change_idx = (swing_data.swing_type.shift(1) != swing_data.swing_type).cumsum()
            new_s = new_swings['swing_type'].astype(str) + swing_change_idx.astype('str')
            new_swings.insert(2, "new_swing_type", new_s, True)
        return new_swings

    def swing_seq_picker(swings_data, swing_type):
        """
        This function manages to remove useless sequential swings in a pandas way
        """
        if swing_type == 'high':
            agg_func = 'max'
        elif swing_type == 'low':
            agg_func = 'min'
        else:
            raise ValueError("Input data must be eigher high or low!")

        duplicate_swings = swings_data.groupby(['new_swing_type']).agg({'swing_value': agg_func})
        return merge(duplicate_swings, swings_data, how="inner", on=["swing_value", 'new_swing_type'])

    def swing_hl_merge(swings_sequential, swings_all):
        """
        This function is responsible for handle high/low swing types.
        It will merge all the high/low swings and will garantee that high/low are sequential.
        """
        if len(swings_sequential) > 0:
            high_swings = swing_seq_picker(swings_sequential[swings_sequential['swing_type'] == 'high'], 'high')
            low_swings = swing_seq_picker(swings_sequential[swings_sequential['swing_type'] == 'low'], 'low')
            swings_high_low = concat([swings_sequential, high_swings, low_swings]).drop_duplicates(keep=False)
            swings_high_low = swings_high_low.reset_index(drop=True)
            del swings_high_low['new_swing_type']
        else:
            swings_high_low = swings_sequential
        swings_high_low = concat([swings_all, swings_high_low]).drop_duplicates(keep=False)
        return swings_high_low

    all_swings = calculate_swings(high, low, pivot_leg)
    all_swings['idx'] = all_swings.index
    swings_seq = swing_seq_catch(all_swings)
    swings_merged = swing_hl_merge(swings_seq, all_swings).reset_index(drop=True)
    swings = swings_merged.reset_index(drop=True)

    while (swings['swing_value'].pct_change().abs() <= price_deviation / 100).any():
        swings_price_dev = price_dev(swings, price_deviation)
        swings_seq_price_dev = swing_seq_catch(swings_price_dev)
        swings_seq_filtered = swing_hl_merge(swings_seq_price_dev, swings_price_dev)
        swings = swings_seq_filtered

    swings.index = swings['idx']
    del swings['idx']

    return all_swings, swings


zigzag.__doc__ = \
""" Zigzag Inddicator

The ZigZag feature on SharpCharts is not an indicator per se, but rather a means to filter out smaller price movements.
A ZigZag set at 10 would ignore all price movements less than 10%; only price movements greater than 10% would be shown.
Filtering out smaller movements gives chartists the ability to see the forest instead of just trees.

Sources:
    https://www.tradingview.com/support/solutions/43000591664-zig-zag/#:~:text=Definition,trader%20visual%20the%20price%20action.
    https://school.stockcharts.com/doku.php?id=technical_indicators:zigzag

Calculation:
    ZigZag (high, low, pivot_leg, price_deviation, retrace=False, LastExtreme=False)
    If  % change > = X, plot ZigZag 
    
    Default Inputs:
        pivot_leg = 5, price_deviation = 10
        retrace = FALSE, LastExtreme = TRUE

    See Source links

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    pivot_leg (int): Initial Acceleration Factor. Default: 5
    price_deviation (float): % change of price. Default: 10
    retrace (Boolean): This can be the change in the retracement of a previous move. Default: False
    Last_extreme (Boolean):  This references extreme price, if it is the same over multiple periods. Default: False

Kwargs:

Returns:
    pd.DataFrame: index of swings, swing_value, and swing_type (high or low).
"""
