# -*- coding: utf-8 -*-
from decimal import Decimal
from functools import partial
from pathlib import Path
from typing import *

from numpy import argmax, argmin, nan, ndarray, recarray, void
from numpy import bool_ as np_bool_
from numpy import floating as np_floating
from numpy import generic as np_generic
from numpy import integer as np_integer
from numpy import number as np_number
from pandas import DataFrame, Series
from sys import float_info as sflt



# Generic types
T = TypeVar("T")

# Scalars
Scalar = Union[str, float, int, complex, bool, object, np_generic]
Number = Union[int, float, complex, np_number, np_bool_]
Int = Union[int, np_integer]
Float = Union[float, np_floating]
IntFloat = Union[Int, Float]

# Basic sequences
MaybeTuple = Union[T, Tuple[T, ...]]
MaybeList = Union[T, List[T]]
TupleList = Union[List[T], Tuple[T, ...]]
MaybeTupleList = Union[T, List[T], Tuple[T, ...]]
MaybeIterable = Union[T, Iterable[T]]
MaybeSequence = Union[T, Sequence[T]]
ListStr = List[str]

DictLike = Union[None, dict]
DictLikeSequence = MaybeSequence[DictLike]
Args = Tuple[Any, ...]
ArgsLike = Union[None, Args]
Kwargs = Dict[str, Any]
KwargsLike = Union[None, Kwargs]
KwargsLikeSequence = MaybeSequence[KwargsLike]
FileName = Union[str, Path]

DTypeLike = Any
PandasDTypeLike = Any
Shape = Tuple[int, ...]
RelaxedShape = Union[int, Shape]
Array = ndarray
Array1d = ndarray
Array2d = ndarray
Array3d = ndarray
Record = void
RecordArray = ndarray
RecArray = recarray
MaybeArray = Union[T, Array]
SeriesFrame = Union[Series, DataFrame]
MaybeSeries = Union[T, Series]
MaybeSeriesFrame = Union[T, Series, DataFrame]
AnyArray = Union[Array, Series, DataFrame]
AnyArray1d = Union[Array1d, Series]
AnyArray2d = Union[Array2d, DataFrame]
