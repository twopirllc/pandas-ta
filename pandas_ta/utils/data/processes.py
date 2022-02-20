
# -*- coding: utf-8 -*-
import datetime as dt
from random import choice as rChoice

from numpy import absolute, any, concatenate, cumsum, flip, max
from numpy import mean, min, ndarray, std, sum, where, zeros
from numpy.random import choice, normal, randint
from pandas import DataFrame, date_range

from pandas_ta._typing import Array, Float, Int, IntFloat, List, Optional
from pandas_ta.maps import Imports, RATE


class sample(object):
    """Sample Data [sample] BETA (Only core features so far)

    DISCLAIMER: Use at your own risk!

    This is a Numpy and stochastics package wrapper Class that easily creates
    stochastic process realization with or without stochastic noise.

    To get the most out of sample(), install the 'stochastic' package:
        $ pip install stochastic

    The following stochastic package noise and processes have been
    implemented:
    * Noise[9]: Blue "b", Brownian "br, Fractal Gaussian "fg", Gaussian "g",
        Pink "p", Red "r", Violet "v", Wiener "w", Random "rand", or None
    * Processes[11]: Brownian Bridge "bb", Brownian Excursion "be",
        Brownian Meander "bm", Brownian Motion "bmo",
        Cox Ingersoll Ross "cir", Fractional Brownian Motion "fbm",
        Geometric Brownian Motion "gbm", Ornstein Uhlenbeck "ou",
        Random Walk "rw", Wiener "w", Random "rand" or None.
    * If the stochastic process is not installed, a Simple Random Walk is
        realized without noise.
    * When argument process="rand", a process is chosen at random.
    * When argument noise="rand", a noise is chosen at random.

    Sources:
        https://stochastic.readthedocs.io/en/stable/

    Args:
        * Basic options
        name (str): Set a ticker name. Default: A random ticker like 'SMPL'.
        process (str): The process to realize. See options above.
            Default: None
        noise (str): Noise to apply. See options above. Default: None
        length (int): How many observations to generate.
            Default: ta.RATE["TRADING_DAYS_PER_YEAR"] (252)

        * Additional transformations
        orient (str): Applies either a Reversal, Inversion or
            Inverted Reversal of the realization. Default: None.
        positive (bool): If the resultant process is non-negative.
            Default: True
        scale (str): Applies either Mean, Normal or Standard scale.
            Default: None.
        noise_percent (float): Percentage of noise to apply. (Not implemented)
            Default: 1.0

        * Arguments specific to the stochastics package
        s0 (float): The initial value of the process. Default: 0.01
        b (float): The "b" argument for Brownian Bridge and Meander.
            Default: 0.01
        t (float): The "t" arguments of certain processes. Default: 0.01
        drift (float): The drift for some processes. For Cox-Ingersoll-Ross,
            mean = drift. Default: 0
        volatility (float): The volatility for some processes. For Brownian
            Motion, scale = volatility. Default: 1
        speed (float): The speed value for some processes. Default: 1
        hurst (float): The Hurst value for Fractional Brownian Motion "fbm".
            Default: 0.5
        steps (list): A list of step increments for the Random Walk.
            Default: [-1, 1]
        random_number (int): Random number for the stochastic package to use.
            Default: None

        * Misc. Options
        future (bool): Whether the resultant DataFrame Index has a future
            date range or a past date range. Default: True
        freq (str): The frequency to use for the generated DataFrame
            date range index. (Not implemented) In Default: "D"
        intraday (str): If intraday is 'full', 24 hours, or is an 'equity'
            with 6.5 hours. (Not implemented) Default: "full"
        date_fmt (str): Date Format for Daterange. Default: '%Y-%m-%d'
        precision (int): How many decimals to round when printing to stdout.
            Default: 6
        verbose (bool): Show more info to stdout. Default: False


    Examples:

    (A) Returns a Brownian Motion Process class instance with initial value
    (s0) 12.34, drift 0.2, scale (volatility) 0.4, t of 5, and random seed of 21
    >>> sp = ta.sample(name="SMPL", process="bmo", s0=12.34, drift=0.2, volatility=0.4, t=5, random_number=21)
    Returns Numpy values of the process
    >>> sp.np
    Returns a DataFrame of the process
    >>> sp.df

    Reverse the process (returns numpy array)
    >>> rev_sp = sp.orientation(sp.np, "r")

    Standard Rescaling of the process (returns numpy array)
    >>> scaled_sp = sp.scale(sp.np, "s")

    Some class properties
    Returns list of processes available
    >>> sp.processes
    Returns selected process
    >>> sp.process
    Returns list of noises available
    >>> sp.noises
    Returns selected noise
    >>> sp.process

    (B) Returns a Random Process and Noise with initial value (s0) 1, positive
    values, inverted, mean scaled and verbose
    >>> rpn = ta.sample(s0=1.0, process="rand", noise="rand", positive=True, orient="i", scale="m", verbose=True)
    >>> rpn.np  # numpy values
    >>> rpn.df  # Pandas DataFrame
    """

    _noises = ["b", "br", "fg", "g", "p", "r", "v", "w", None, "rand"]
    _orientations = ["i", "r", "ir", "ri", None, "rand"]
    _processes = [
        "bb", "be", "bm", "bmo", "cir", "fbm",
        "gbm", "ou", "rw", "w", None, "rand"
    ]
    _scales = ["m", "n", "s", None]

    def __init__(self,
        name: str = None, process: str = None, noise: str = None,
        length: Int = None, s0: IntFloat = None, b: IntFloat = None,
        t: IntFloat = None, drift: Int = None, volatility: IntFloat = None,
        speed: IntFloat = None, hurst: Float = None,
        steps: List[IntFloat] = None, random_number: Optional[Int] = None,
        orient: str = None, positive: bool = None, scale: str = None,
        future: bool = None, freq: str = None, intraday: str = None,
        noise_percent: Float = None, date_fmt: str = None,
        precision: Int = None, verbose: bool = None
    ):
        """Validation and initialization of arguments and then runs the
        _generate() method to build a sample realization with the given
        arguments.
        """
        _random_symbol = ''.join(
            [rChoice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(randint(3, 6))])
        self._name = str(name) if name is not None and isinstance(
            name, str) else _random_symbol
        self._process = str(process).lower() if process is not None and isinstance(
            process, str) and process in self._processes else None
        self._noise = str(noise).lower() if noise is not None and isinstance(
            noise, str) and noise in self._noises else None
        self._length = int(length) if isinstance(
            length, int) else RATE["TRADING_DAYS_PER_YEAR"]

        self._s0 = float(s0) if s0 is not None and isinstance(
            s0, (float, int)) else 0.01
        self._b = float(b) if b is not None and isinstance(b, float) else 0.0
        self._t = float(t) if t is not None and isinstance(
            t, (float, int)) else 1.0
        self._drift = float(drift) if drift is not None and isinstance(
            drift, (float, int)) else 0.0
        self._volatility = float(volatility) if volatility is not None and isinstance(
            volatility, (float, int)) else 1.0
        self._speed = float(speed) if speed is not None and isinstance(
            speed, (float, int)) else 1.0
        self._hurst = float(hurst) if hurst is not None and isinstance(
            hurst, float) and 0 <= hurst <= 1 else 0.5
        self._steps = steps if steps is not None and isinstance(
            steps, list) and len(steps) > 1 else [-1.0, 1.0]
        self._random_number = random_number if random_number is not None else None

        self._orient = str(orient).lower() if orient is not None and isinstance(
            orient, str) and orient in self._orientations else None
        self._positive = positive if positive is not None and isinstance(
            positive, bool) else False
        self._scale = str(scale).lower() if scale is not None and isinstance(
            scale, str) and scale in self._scales else None

        self._future = future if future is not None and isinstance(
            future, bool) else False
        self._freq = f"{freq.lower()}" if freq is not None and len(
            freq) else "D"
        self._intraday = intraday.lower() if intraday is not None and len(
            intraday) and intraday in ["full", "equity"] else "full"

        self._noise_percent = float(noise_percent) if noise_percent is not None and isinstance(
            noise_percent, float) else 1.0  # Percent as decimal
        _date_fmt = str(noise) if date_fmt is not None and isinstance(
            date_fmt, str) else "%Y-%m-%d"
        self._date_today = dt.date.today().strftime(_date_fmt)
        self._precision = int(precision) if precision is not None and isinstance(
            precision, int) else 6
        self._verbose = verbose if verbose is not None and isinstance(
            verbose, bool) else False

        if self._process == "rand":
            self._process = choice(self._processes[:-2])

        if self._noise == "rand":
            self._noise = choice(self._noises[:-1])

        self._generate()  # Run it

    def _bernoulli_mask(self,
        array: Array, percent: Float = None, p: Float = None
    ):
        """Bernoulli Mask - Positive or Negative"""
        if array.size > 0:
            percent = float(percent) if percent is not None and isinstance(
                percent, float) else self.noise_percent
            p = float(p) if p is not None and isinstance(
                p, float) and p > 0 and p < 1 else 0.5
            return array * self.noise_percent * self._bernoulli_process()
        return array

    def _bernoulli_process(self):
        """Bernoulli Process"""
        return randint(2, size=self.length)

    def _generate(self):
        """A method to generate stochastic process realizations.

        Order of operations:
        1. Generate a stochastic process and noise if not None and combine.
        2. Reorient original realization is not None.
        3. Make realization non-negative if an values are <= 0 if the
            'positive' argument is True.
        4. Recale the realization if the not None.
        5. Save the result to self._np.
        """
        values = self._stoch_process()
        values += self._stoch_noise()

        if self._orient is not None and isinstance(self._orient, str):
            values = self._orientation(values, mode=self._orient)
            if self._verbose:
                print(f"[i] Orientation: {self._orient}")

        if self.positive:
            _s0 = values[0]
            values = self._nonnegative(values)
            if self._verbose:
                print(
                    f"[i] New s0: {round(values[0], self._precision)} from {round(_s0, self._precision)} (change {round(values[0] - _s0, self._precision)})")

        if self._scale is not None and isinstance(self._scale, str):
            values = self._scaler(values, self._scale)
            if self._verbose:
                print(f"[i] Scaled to: {self._scale}")

        self._np = values

        _npns = f"{self.name} | {self.process} {self.noise+' ' if self.noise is not None else ''}{self.np.size}"
        _s0n = f"s0: {round(self.np[0], self._precision)}, sN: {round(self.np[-1], self._precision)}"
        _msmm = f"mu: {round(mean(self.np), self._precision)}, sigma: {round(std(self.np), self._precision)}"
        self._dfname = f"{_npns} | {_s0n} | {_msmm}"
        if self._verbose:
            print(self._dfname)

    def nonnegative(self, array: Array = None):
        """Vertical Translation the 'array' where the resultant 'array' has
        non-negative values."""
        if isinstance(array, ndarray):
            return self._nonnegative(array)
        return array

    def _nonnegative(self, array: Array):
        """Translates the array up by the minimum of the 'array' if any values
        are negative."""
        if array.size > 0 and any(array < 0):
            array += -1 * array.min()
            self._s0 = array[0]
        return array

    def _normal_mask(self, array: Array):
        """A method to add some additional randomness to the realized
        process. Applies a mask based on the Normal Distribution and the 'array's
        mean and standard deviation."""
        if array.size > 0:
            norm = normal(mean(array), std(array), size=self.length)
            return array * self.noise_percent * norm
        return array

    def orientation(self, array: Array, mode: str = None):
        """Orients the 'array' either by Inversion, Reversal, or an
        Inverted Reversal."""
        if isinstance(array, ndarray):
            return self._orientation(array, mode=mode)
        return array

    def _orientation(self, array: Array, mode: str = None):
        """Orients the 'array' either by Inversion, Reversal, or an
        Inverted Reversal."""
        _modes = ["i", "r", "ir", "ri", None, "rand"]
        mode = str(mode).lower() if mode is not None and isinstance(
            mode, str) and mode.lower() in _modes else None

        result = array
        if mode is None:
            return result
        if mode == "rand":
            mode = choice(_modes[3:])

        if mode == "i":
            mid = 0.5 * (min(array) + max(array))
            inv = mid - array
            diff = inv - inv[0]
            result = array[0] + diff if array[0] > 0 else diff - array[0]

        if mode == "r":
            result = flip(array) - (array[-1] - array[0])

        if mode in ["ir", "ri"]:
            result = self._orientation(self._orientation(array, "i"), "r")

        return result

    def scale(self, array: Array, mode: str):
        """Mean, Normal or Standard scaling of the 'array'."""
        if isinstance(array, ndarray):
            return self._scaler(array, mode=mode)
        return array

    def _scaler(self, array: Array, mode: str):
        """Scaling: mean, normal, standard"""
        result = array
        if mode is None:
            return result
        if mode == "rand":
            mode = choice(self._scales[3:])

        min_, max_ = min(array), max(array)
        range_ = absolute(max_ - min_)
        mu_, std_ = mean(array), std(array)

        if mode == "m" and range_ > 0:  # "mean"
            result = ((array - mu_) / range_)

        if mode == "n" and range_ > 0:  # "normal"
            result = ((array - min_) / range_)

        if mode == "s" and std_ > 0:  # "standard"
            result = ((array - mu_) / std_)

        return result

    def _simple_random_walk(self,
            up: Float = None, down: Float = None
    ) -> Array:
        """Simple Random Walk

        Sources:
            https://sphelps.net/teaching/scf/slides/random-walks-slides.html
        """
        up = float(up) if up is not None and isinstance(
            up, (int, float)) else 1.0
        down = float(down) if down is not None and isinstance(
            down, (int, float)) else -1.0
        if up < down:
            down, up = up, down

        x = concatenate(([0.0],
             where(randint(0, 2, size=self.length - 1) == 0, down, up)
        ))
        return cumsum(x).astype(float)

    def _stoch_noise(self):
        """Method to apply noise from the stochastic package if installed.
        Otherwise, it returns 0 noise.
        """
        _desc = f"[+] "
        result = zeros(self.length, dtype=float)

        if self._noise is not None and Imports["stochastic"]:
            from stochastic import random as st_random
            st_random.use_generator()
            st_random.seed(self.random_number)

            if self._noise in ["blue", "b"]:
                from stochastic.processes.noise import BlueNoise
                result = BlueNoise(t=self.t).sample(self.length - 1)
                _desc += f"Blue Noise [blue|b] | t: {self.t}"
            elif self._noise in ["brownian", "br"]:
                from stochastic.processes.noise import BrownianNoise
                result = BrownianNoise(t=self.t).sample(self.length - 1)
                _desc += f"Brownian Noise [brownian|br] | t: {self.t}"
            elif self._noise in ["fractional", "fg"]:
                from stochastic.processes.noise.fractional_gaussian_noise import FractionalGaussianNoise
                result = FractionalGaussianNoise(
                    hurst=self.hurst, t=self.t).sample(
                    self.length)
                _desc += f"Fractional Gaussian Noise [fractal|fg] | hurst: {self.hurst}, t: {self.t}"
            elif self._noise in ["gauss", "g"]:
                from stochastic.processes.noise import GaussianNoise
                result = GaussianNoise(t=self.t).sample(self.length)
                _desc += f"Gaussian Noise [gauss|g] | t: {self.t}"
            elif self._noise in ["pink", "p"]:
                from stochastic.processes.noise import PinkNoise
                result = PinkNoise(t=self.t).sample(self.length - 1)
                _desc += f"Pink Noise [pink|p] | t: {self.t}"
            elif self._noise in ["red", "r"]:
                from stochastic.processes.noise import RedNoise
                result = RedNoise(t=self.t).sample(self.length - 1)
                _desc += f"Red Noise [red|r] | t: {self.t}"
            elif self._noise in ["violet", "v"]:
                from stochastic.processes.noise import VioletNoise
                result = VioletNoise(t=self.t).sample(self.length - 1)
                _desc += f"Violet Noise [violet|v] | t: {self.t}"
            elif self._noise in ["white", "w"]:
                from stochastic.processes.noise import WhiteNoise
                result = WhiteNoise(t=self.t).sample(self.length - 1)
                _desc += f"White Noise [white|w] | t: {self.t}"
            else:
                _desc = "Noiseless"

        else:  # Default if no stochastic package installed
            _desc = "srw"

        # Initial Value (s0) adjustment
        result = result + \
            result[0] if result[0] > self.s0 else result - result[0]

        if result is not None and any(result) and self._verbose:
            print(_desc)

        return result

    def _stoch_process(self):
        """Method to return some realizations from the stochastic package.
        Otherwise, it returns a Simple Random Walk."""
        _desc = f"[+] "
        result = None
        if self._process is not None and Imports["stochastic"]:
            from stochastic import random as st_random
            st_random.use_generator()
            st_random.seed(self.random_number)

            if self._process == "bb":
                from stochastic.processes.continuous import BrownianBridge
                result = self.s0 + \
                    BrownianBridge(b=self.b, t=self.t).sample(self.length - 1)
                _desc += f"Brownian Bridge [bb] | s0: {self.s0}, b: {self.b}, t: {self.t}"
            elif self._process == "be":
                from stochastic.processes.continuous import BrownianExcursion
                result = self.s0 + \
                    BrownianExcursion(t=self.t).sample(self.length - 1)
                _desc += f"Brownian Excursion [be] | s0: {self.s0}, t: {self.t}"
            elif self._process == "bm":
                from stochastic.processes.continuous import BrownianMeander
                result = self.s0 + \
                    BrownianMeander(t=self.t).sample(self.length - 1, self.b)
                _desc += f"Brownian Meander [bm] | s0: {self.s0}, t: {self.t}"
            elif self._process == "bmo":
                from stochastic.processes.continuous import BrownianMotion
                result = self.s0 + BrownianMotion(
                    drift=self.drift,
                    scale=self.volatility,
                    t=self.t).sample(
                    self.length - 1)
                _desc += f"Brownian Motion [bmo] | s0: {self.s0}, drift: {self.drift}, scale: {self.volatility}, t: {self.t}"
            elif self._process == "cir":
                from stochastic.processes.diffusion import CoxIngersollRossProcess
                result = CoxIngersollRossProcess(
                    speed=self.speed,
                    mean=self.drift,
                    vol=self.volatility,
                    t=self.t).sample(
                    self.length - 1,
                    self.s0)
                _desc += f"Cox Ingersoll Ross [cir] | s0: {self.s0}, speed: {self.speed}, mean: {self.drift}, vol: {self.volatility}, t: {self.t}"
            elif self._process == "fbm":
                from stochastic.processes.continuous import FractionalBrownianMotion
                result = self.s0 + \
                    FractionalBrownianMotion(
                        hurst=self.hurst, t=self.t).sample(
                        self.length - 1)
                _desc += f"Fractal Brownian Motion [fbm] | s0: {self.s0}, hurst: {self.hurst}, t: {self.t}"
            elif self._process == "gbm":
                from stochastic.processes.continuous import GeometricBrownianMotion
                result = GeometricBrownianMotion(
                    drift=self.drift,
                    volatility=self.volatility,
                    t=self.t).sample(
                    self.length - 1,
                    self.s0)
                _desc += f"Geometric Brownian Motion [gbm] | s0: {self.s0}, drift: {self.drift}, vol: {self.volatility}, t: {self.t}"
            elif self._process == "ou":
                from stochastic.processes.diffusion import OrnsteinUhlenbeckProcess
                result = OrnsteinUhlenbeckProcess(
                    speed=self.speed, vol=self.volatility, t=self.t).sample(
                    self.length - 1, self.s0)
                _desc += f"Ornstein Uhlenbeck [ou] | s0: {self.s0}, speed: {self.speed}, vol: {self.volatility}, t: {self.t}"
            elif self._process == "rw":
                from stochastic.processes.discrete import RandomWalk
                result = self.s0 + \
                    RandomWalk(
                        steps=self.steps).sample(
                        self.length -
                        1).astype(float)
                _desc += f"Random Walk [rw] |  s0: {self.s0}, steps: {self.steps}"
            elif self._process == "w":
                from stochastic.processes.continuous import WienerProcess
                result = self.s0 + \
                    WienerProcess(t=self.t).sample(self.length - 1)
                _desc += f"Wiener [w] | s0: {self.s0},  t: {self.t}"

        else:  # Default if no stochastic package installed
            result = self.s0 + self._simple_random_walk()
            _desc += f"Simple Random Walk | s0: {self.s0}"

        if result is not None and self._verbose:
            print(_desc)

        return result

    @property
    def b(self):
        """The 'b' value for some stochastic processes."""
        return self._b

    @property
    def datetime_range(self):
        """The Pandas datetimerange used by the resultant DataFrame index."""
        if hasattr(self, "_datetimerange") and self._datetimerange is not None:
            return self._datetimerange
        else:
            self._datetimerange = None
            # datelist = date_range(date_N_days_ago, periods=N, freq=freq).to_pydatetime().tolist()
            if self.future:
                self._datetimerange = date_range(
                    start=self._date_today, periods=self.length, freq=self.freq)
            else:
                self._datetimerange = date_range(
                    end=self._date_today, periods=self.length, freq=self.freq)

        return self._datetimerange

    @property
    def df(self):
        """The Pandas DataFrame of the sample/realization."""
        if self.np is not None and self.np.size > 0:
            df = DataFrame(
                self.np,
                index=self.datetime_range,
                columns=["close"])
            df.name = self._dfname
            self._df = df
            return self._df
        return None

    @property
    def drift(self):
        """The 'drift' value for some stochastic processes."""
        return self._drift

    @property
    def freq(self):
        """The frequency of the Pandas daterange."""
        return self._freq

    @property
    def future(self):
        """Whether the Pandas daterange DataFrame index has future values or
        past values from today."""
        return self._future

    @property
    def hurst(self):
        """The 'Hurst' value for Fractional Brownian Motion 'fbm'."""
        return self._hurst

    @property
    def length(self):
        """The length of the sample/realization."""
        return self._length

    @property
    def name(self):
        """The name of the sample/realization.
            If not set, randomly generated with prefix '~'.
        """
        return self._name

    @property
    def noise(self):
        """Noise sample/realization."""
        return self._noise

    @property
    def noise_percent(self):
        """Percent to apply to noise."""
        return self._noise_percent

    @property
    def noises(self):
        """List of available noises in the class."""
        return self._noises

    @property
    def np(self):
        """The Numpy values of the sample/realization."""
        return self._np

    @property
    def orient(self):
        """The orientation applied when generated."""
        return self._orient

    @property
    def positive(self):
        """Enforce non-negative values of the sample/realization."""
        return self._positive

    @property
    def process(self):
        """Process sample/realization."""
        return self._process

    @property
    def processes(self):
        """List of available processes in the class."""
        return self._processes

    @property
    def random_number(self):
        """Random Number of the sample/realization."""
        return self._random_number

    @property
    def s0(self):
        """The initial value of the stochastic process."""
        return self._s0

    @property
    def speed(self):
        """The 'speed' value for some stochastic processes."""
        return self._speed

    @property
    def steps(self):
        """The 'steps' value for Random Walk."""
        return self._steps

    @property
    def t(self):
        """The 't' value for some stochastic processes."""
        return self._t

    @property
    def volatility(self):
        """The 'volatility' value for some stochastic processes."""
        return self._volatility
