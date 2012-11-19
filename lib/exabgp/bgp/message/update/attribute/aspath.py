# encoding: utf-8
"""
aspath.py

Created by Thomas Mangin on 2009-11-05.
Copyright (c) 2009-2012 Exa Networks. All rights reserved.
"""

from exabgp.bgp.message.update.attribute.id import AttributeID
from exabgp.bgp.message.update.attribute import Flag,Attribute

# =================================================================== ASPath (2)

class ASPath (Attribute):
	AS_SET      = 0x01
	AS_SEQUENCE = 0x02

	ID = AttributeID.AS_PATH
	FLAG = Flag.TRANSITIVE
	MULTIPLE = False

	def __init__ (self,as_sequence,as_set,index=None):
		self.as_seq = as_sequence
		self.as_set = as_set
		self.segments = ''
		self.packed = {True:'',False:''}
		self.index = index  # the original packed data, use for indexing
		self._str = ''

	def _segment (self,seg_type,values,asn4):
		l = len(values)
		if l:
			if l>255:
				return self._segment(seg_type,values[:255]) + self._segment(seg_type,values[255:])
			return "%s%s%s" % (chr(seg_type),chr(len(values)),''.join([v.pack(asn4) for v in values]))
		return ""

	def _segments (self,asn4):
		segments = ''
		if self.as_seq:
			segments = self._segment(self.AS_SEQUENCE,self.as_seq,asn4)
		if self.as_set:
			segments += self._segment(self.AS_SET,self.as_set,asn4)
		return segments

	def pack (self,asn4):
		if not self.packed[asn4]:
			self.packed[asn4] = self._attribute(self._segments(asn4))
		return self.packed[asn4]

	def __len__ (self):
		raise RuntimeError('it makes no sense to ask for the size of this object')

	def __str__ (self):
		if not self._str:
			lseq = len(self.as_seq)
			lset = len(self.as_set)
			if lseq == 1 and not lset:
				string = '%d' % self.as_seq[0]
			elif lseq > 1 :
				if lset:
					string = '[ %s %s]' % ((' '.join([str(_) for _ in self.as_seq])),'( %s ) ' % (' '.join([str(_) for _ in self.as_set])))
				else:
					string = '[ %s ]' % ' '.join([str(_) for _ in self.as_seq])
			else:  # lseq == 0
				string = '[ ]'
			self._str = string
		return self._str

class AS4Path (ASPath):
	ID = AttributeID.AS4_PATH
	FLAG = Flag.TRANSITIVE|Flag.OPTIONAL

	def pack (self):
		ASPath.pack(self,True)