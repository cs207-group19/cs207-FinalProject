import numpy as np

# Change built-in warnings to exceptions when using numpy
np.seterr(all='raise')

class Var(object):
	def __init__(self, values, der=None):
		"""
		a: input as a list, transform it into np.array
		"""
		if isinstance(values, float) or isinstance(values, int):
			values = [values]
		if der is None:
			der = np.ones_like(values)
		elif isinstance(der, float) or isinstance(der, int):
			der = [der]
		self.val = np.array(values)
		self.der = np.array(der)
	
	def __repr__(self):
		return 'Var({}, {})'.format(self.val, self.der)

	def __add__(self, other):
		val = self.val
		der = self.der
		try:
			val += other.val
			der += other.der
		except AttributeError:
			val += other
		return Var(val, der)
	
	def __radd__(self, other):
		return self.__add__(other)
		
	def __mul__(self, other):
		val = self.val
		der = self.der
		try:            
			val = val * other.val          
			der = der * other.val + val * other.der
		except AttributeError:
			val = val * other
			der = der * other
		return Var(val, der)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __truediv__(self, other):
		val = self.val
		der = self.der
		try:
			val = np.divide(val, other.val)
			der = (np.multiply(other.val, der) - np.multiply(val, other.der)) / (other.val ** 2)
		except AttributeError:
			val = np.divide(val, other)
			der = np.divide(der, other)
		return Var(val, der)

	def __rtruediv__(self, other):
		'''Note: self contains denominator; other contains numerator'''
		try:
			val = np.divide(other.val, self.val)
			der = (np.multiply(self.val, other.der) - np.multiply(other.val, self.der)) / (np.linalg.norm(self.val) ** 2)
		except AttributeError:
			val = np.divide(other, self.val)
			der = (-np.multiply(other, self.der)) / (np.linalg.norm(self.val) ** 2)
		return Var(val, der)

	def sin(self):
		val = np.sin(self.val)
		der = np.cos(self.val) * self.der
		return Var(val, der)

	def cos(self):
		val = np.cos(self.val)
		der = -np.sin(self.val) * self.der
		return Var(val, der)
	
	def tan(self):
		# Ensure that no values in self.val are of the form (pi/2 + k*pi)        
		values = map(lambda x: ((x % np.pi) - 0.5) % 1 == 0.0, self.val)
		if any(values):
		#if abs(self.val) >= np.pi/2 and any(values):
			raise ValueError("Tangent not valid at pi/2, -pi/2.")
		val = np.tan(self.val)
		der = np.multiply(np.power(1 / np.cos(self.val), 2), self.der)
		return Var(val, der)

	def arcsin(self):
		values = map(lambda x: -1 <= x <= 1, self.val)
		if not all(values):
			raise ValueError("Range of arcsin is [-1, 1].")		
		val = np.arcsin(self.val)
		der = 1 / np.sqrt(1 - (self.val ** 2))
		return Var(val, der)

	def arccos(self):
		values = map(lambda x: -1 <= x <= 1, self.val)
		if not all(values):
			raise ValueError("Range of arccos is [-1, 1].")	
		val = np.arccos(self.val)
		der = -1 / np.sqrt(1 - (self.val ** 2))
		return Var(val, der)

	def arctan(self):
		val = np.arctan(self.val)
		der = 1 / (1 + (self.val) ** 2)
		return Var(val, der)
 
	def sinh(self):
		val = np.sinh(self.val)
		der = np.cosh(self.val)
		return Var(val, der) 

	def cosh(self):
		val = np.cosh(self.val)
		der = np.sinh(self.val)
		return Var(val, der)

	def tanh(self):
		val = np.tanh(self.val)
		der = 1 / np.power(np.cosh(self.val), 2)
		return Var(val, der)

	def pow(self, n):
		values = map(lambda x: x >= 0, self.val)
		if n % 1 != 0 and not all(values):
			raise ValueError("Non-positive number raised to a fraction encountered in pow.")
		elif n < 1 and 0 in self.val:
			raise ZeroDivisionError("Cannot compute derivative of 0^y for y < 1.")

		val = np.power(self.val, n)
		der = n * np.multiply((self.val ** (n - 1)), self.der)
		return Var(val, der)

	def log(self, base):
		values = map(lambda x: x > 0, self.val)
		if not all(values):
			raise ValueError("Non-positive number encountered in log.")
		else:
			val = np.math.log(self.val, base)
			der = np.multiply(np.divide(np.log(base), self.val), self.der)
		return Var(val, der)

	def exp(self):
		val = np.exp(self.val) 
		der = np.multiply(np.exp(self.val), self.der)
		return Var(val, der)