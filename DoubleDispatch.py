"""A concrete application of the (badly named) Visitor Pattern, which should
actually be called Double Dispatch Pattern.

Notes:

1. When a new concrete Graphic, say a Rectangle class, is implemented:
a) add an ABSTRACT dispatcher method to the Dispatcher ABC that the Rectangle
   class should dispatch to (and give it a meaningful name:
   
	class Graphics(ABC):
		...
  
		@abstractmethod
        def dispatch_rect(self, rect: Rectangle) -> None;
            pass
        
b) implement the dispatch_rect() method in ALL existing concrete dispatcher
   classes.
c) the Rectangle class must implement all abstract methods from Graphics ABC,
   including the accept() method:
   
	class Rectangle(Graphics):
		...
		
		def accept(self, dispatcher: Dispatcher) -> None:
		    dispather.dispatch_rect(self)

2. When a new concrete Dispatcher, say PDFExportDispatcher, is implemented:
a) a dispatcher method must be implemented for each concrete graphics
   implementation (names of these methods are already fixed).
   
    class PDFExportDispatcher(Dispatcher):
        ...
        
        def dispatch_dot(self, dot: Dot):
            # implementation of the PDF export of a dot, called by dot.accept
            # when dot.accept(PFDExportDispatcher) is called by client.
            ...
            
        def dispatch_circle(self, dot: Dot):
            # implementation of the PDF export of a circle, called by
            # circle.accept when circle.accept(PFDExportDispatcher) is called
            # by client.
            ...
            
        def dispatch_rect(self, dot: Dot):
            # implementation of the PDF export of a rectangle, called by
            # rectangle.accept when rectangle.accept(PFDExportDispatcher) is
            # called by client.
            ...
	
b) Notice that NO modifications are required on any of the existing graphics
   classes!

3. This pattern is useful if classes need to support functionality that is not
   really supposed to be part of the class, or if modifying classes by
   implementing new functionality is not an option (too risky)."""

from __future__ import annotations
from abc import ABC, abstractmethod


class Graphics(ABC):
	"""The Graphics interface declares an accept() method that should take the
	base dispatcher interface as an argument."""
	
	@abstractmethod
	def accept(self, dispatcher: Dispatcher) -> None:
		"""This method allows for double dispatching and must be implemented by
		concrete implementations of Graphics ABC. It should call the specific
		method on the dispatcher object for the concrete graphic class."""
		
		pass
	
	@abstractmethod
	def draw(self) -> None:
		"""Must be implemented by concrete implementations."""
		
		pass


class Dot(Graphics):
	"""A dot is a concrete implementation of the Graphics ABC."""
	
	def __init__(self, x: int, y: int) -> None:
		"""Each dot has an x and y coordinate in a two dimensional plane."""
		
		self.x = x
		self.y = y
	
	def accept(self, dispatcher: Dispatcher) -> None:
		"""Each concrete class that derives from graphics must implement the
		accept() method in such a way that it calls the dispatcher's method
		corresponding to the concrete class."""
		
		dispatcher.dispatch_dot(self)
	
	def draw(self) -> None:
		"""Implementation for drawing a Dot instance."""
		
		print(f"Drawing {self!r}")
	
	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.x}, {self.y})"


class Circle(Graphics):
	"""A circle is a concrete implementation of the Graphics ABC."""
	
	def __init__(self, dot: Dot = Dot(0, 0), radius: int = 1) -> None:
		"""Each circle has a dot as its centre, and a radius. If no centre is
		supplied, we take the origin as centre, and if no radius is supplied we
		take the unit radius. Ergo: Circle() creates the unit circle."""
		
		self.centre = dot
		self.radius = radius
	
	def accept(self, dispatcher: Dispatcher) -> None:
		"""Each concrete class that derives from graphics must implement the
		accept() method in such a way that it calls the dispatcher's method
		corresponding to the concrete class."""
		
		dispatcher.dispatch_circle(self)
	
	def draw(self) -> None:
		"""Implementation for drawing a Circle instance."""
		
		print(f"Drawing {self!r}")

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.centre!r}, {self.radius!r})"


class Dispatcher(ABC):
	"""An abstract dispatch method should be declared for each concrete
	implementation of Graphics ABC (that is, each class that inherits from and
	implements Graphics ABC). Each concrete implementation of the Dispatcher
	ABC must implement each of these methods. See XMLExportDispatcher and
	JSONExportDispatcher, which implement XML export and JSON export,
	respectively)."""
	
	@abstractmethod
	def dispatch_dot(self, dot: Dot) -> None:
		"""Must be implemented by concrete implementations."""
		
		pass
	
	@abstractmethod
	def dispatch_circle(self, circle: Circle) -> None:
		"""Must be implemented by concrete implementations."""
		
		pass


class XMLExportDispatcher(Dispatcher):
	"""A concrete implementation of the Dispatcher ABC. NOTICE that for the
	implementation of XML export, NO changes to any of the Graphics classes
	are needed! All that is required is an implementation of the accept()
	method on each concrete Graphics implementation. Once the accept method is
	there, classes like XMLExportDispatcher and JSONExportDispatcher can be
	implemented WIHOUT any further changes to the existing concrete Graphics
	classes."""

	def dispatch_dot(self, dot: Dot) -> None:
		"""This method is called by dot.accept(XMLExportDispatcher)."""
		
		print(f"XMLExporting {dot.__class__.__name__}({dot.x}, {dot.y})")
	
	def dispatch_circle(self, circle: Circle) -> None:
		"""This method is called by circle.accept(XMLExportDispatcher)."""

		print(f"XMLExporting {circle.__class__.__name__}"
		      f"({circle.centre}, {circle.radius})")

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}()"


class JSONExportDispatcher(Dispatcher):
	"""A concrete implementation of the Dispatcher ABC. NOTICE that for the
	implementation of JSON export, NO changes to any of the Graphics classes
	are necessary! All that is required is an implementation of the accept()
	method on each concrete Graphics implementation. Once the accept method is
	there, classes like XMLExportDispatcher and JSONExportDispatcher can be
	implemented WITHOUT any further changes to the existing concrete Graphics
	classes."""

	def dispatch_dot(self, dot: Dot) -> None:
		"""This method is called by dot.acceptJSONExportDispatcher)."""
		
		print(f"JSONExporting {dot.__class__.__name__}({dot.x}, {dot.y})")
	
	def dispatch_circle(self, circle: Circle) -> None:
		"""This method is called by circle.acceptJSONExportDispatcher)."""
		
		print(f"JSONExporting {circle.__class__.__name__}"
		      f"({circle.centre}, {circle.radius})")

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}()"


if __name__ == "__main__":
	
	def _main() -> None:
		graphics = [dot := Dot(10, 20), Circle(dot, 11), Circle()]
		for graphic in graphics:
			graphic.draw()
		
		exporters = [XMLExportDispatcher(), JSONExportDispatcher()]
		for exporter in exporters:
			for graphic in graphics:
				graphic.accept(exporter)

	_main()
