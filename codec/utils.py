import codec.custom_types

def makeComplex(l):
   res = custom_types.hashdict()
   for  i in range(0, len(l), 2):
      k = l[i]
      if isinstance(k, dict):
         k = custom_types.hashdict(k)
      res[k] = l[i+1]
   return res
