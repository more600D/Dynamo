class ModelUpdatesStatus(Enum,IComparable,IFormattable,IConvertible):
 """
 Indicates whether an element in the current model has additional user changes in the central model.

 

 enum ModelUpdatesStatus,values: CurrentWithCentral (0),DeletedInCentral (2),NotYetInCentral (1),UpdatedInCentral (3)
 """
 def __eq__(self,*args):
  """ x.__eq__(y) <==> x==yx.__eq__(y) <==> x==yx.__eq__(y) <==> x==y """
  pass
 def __format__(self,*args):
  """ __format__(formattable: IFormattable,format: str) -> str """
  pass
 def __ge__(self,*args):
  pass
 def __gt__(self,*args):
  pass
 def __init__(self,*args):
  """ x.__init__(...) initializes x; see x.__class__.__doc__ for signaturex.__init__(...) initializes x; see x.__class__.__doc__ for signaturex.__init__(...) initializes x; see x.__class__.__doc__ for signature """
  pass
 def __le__(self,*args):
  pass
 def __lt__(self,*args):
  pass
 def __ne__(self,*args):
  pass
 def __reduce_ex__(self,*args):
  pass
 def __str__(self,*args):
  pass
 CurrentWithCentral=None
 DeletedInCentral=None
 NotYetInCentral=None
 UpdatedInCentral=None
 value__=None

