class Float32(float):
   pass

class hashdict(dict):
   def __key(self):
      return tuple(sorted(self.items()))
   def unsortKey(self):
      return tuple(self.items())
   def __repr__(self):
      return "{0}({1})".format(self.__class__.__name__,
                               ", ".join("{0}={1}".format(
                                  str(i[0]),repr(i[1])) for i in self.unsortKey()))

   def __hash__(self):
      return hash(self.__key())

   def __lt__(self, other):
      return len(self) < len(other) or self.__key() < other.__key()

   def __eq__(self, other):
      return self.__key() == other.__key()
