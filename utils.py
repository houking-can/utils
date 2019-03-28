#!/usr/bin/env python3
# Copyright 2019-present, DataHammber, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Common utils for processing data."""

import os

def iter_files(path):
	"""Walk through all files located under a root path."""
	if os.path.isfile(path):
		yield path
	elif os.path.isdir(path):
		for dirpath, _, filenames in os.walk(path):
			for f in filenames:
				yield os.path.join(dirpath, f)
	else:
		raise RuntimeError('Path %s is invalid' % path)

def permutation(nums):
	"""
	generate permutation of nums
	:type deck: List[int]
	:rtype: List[List[int]]
	nums = [1,2,3]
	print(permutation(nums))
	"""
	if len(nums)==0: return [[]]
	result = []
	for i in range(len(nums)):
		select = nums[:i]+nums[i+1:]
		for x in permutation(select):
			result += [nums[i:i+1]+x]
	return result


def combination(nums, r):
	"""
	generate r subset of nums
	:type deck: List[int] 
	:type k: int
	:rtype: List[List[int]]
	nums = [1,2,3]
	print(permutation(nums))
	"""
	if r == 0: return [[]]
	result = []
	for i in range(len(nums)):
		for x in combination(nums[i+1:], r-1):
			result += [nums[i:i+1] + x]
	return result
